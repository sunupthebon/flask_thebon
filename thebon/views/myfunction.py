# from flask import Flask, render_template, request, redirect, url_for

from thebon.views import cosine_test9
from googleapiclient.discovery import build
from urllib.request import HTTPError, URLError
import pandas as pd
from GoogleNews import GoogleNews
import newspaper
from newspaper import Article, Config
import requests

import nltk

from googletrans import Translator  # 기본 구글 번역
# from google.cloud import translate
# from google.cloud import translate_v3beta1 as translate
from google.cloud import translate_v2 as translate
# import six from google.cloud
# import translate_v2 as translate

# 내부서버 환경입니다
from fake_useragent import UserAgent

def more_info(article_url) :

    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    ua = UserAgent(verify_ssl=False)
    user_agent = ua.random
    print(user_agent)

    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 10    
    article = Article(article_url, config=config)

    try:
            article.download()
            print("article.download() succeed")
            article.parse()
            print("article.parse() succeed")
            article.nlp()
            print("article.nlp() succeed")
            
    except newspaper.article.ArticleException as ae:
            print("article download parse nlp failed")
            print(ae)
            
    if not article.summary:
        print("article.summary가 비었습니다")
        return (" ", "Sorry. I failed to get the document.")
    else:
        print(article.summary)
        trans_summary = papago_translate(article.summary, 'ko')
        print(trans_summary)
        return (article.summary, trans_summary)
  

def crawling_main_fun(search_word):
    good_array = {}
    bad_array = {}

    dateRestrict = 'd1'
    search_pages = 10
    init_connect()
    main_good_datas = crawl_article(search_word, dateRestrict, search_pages)

    if len(main_good_datas.index) == 0:
        print("검색결과가 없습니다")
        # return render_template("search.html")
        return main_good_datas
    else:
        print(main_good_datas)
        # main_good_datas = google_search.article_download(main_good_datas)

        # 코싸인 유사도 확인해서 중복 데이터 제거
        main_good_datas = cosine_test9.my_cosine_similarity(main_good_datas, 'snippet')
        #main_good_datas = cosine_test9.my_cosine_similarity3(main_good_datas)

        #  snippet의 코싸인 유사도 확인해서 중복 데이터 제거

        # 번역본 붙이기
        article_transfer(main_good_datas, 'snippet', 2)
        # google_news_search05.my_save_to_excel("crawl_snippet "+search_word, main_good_datas, t)
        # print(main_good_datas)

        # google_search.article_transfer(main_good_datas, 'summary', 4)
        # google_news_search05.my_save_to_excel("crawl_summary "+search_word, main_good_datas, t)
        # print(main_good_datas)

        #         #불필요한 컬럼 지우기
        # #        main_good_datas.drop(columns=['title', 'summary_idx'], inplace = True) # inplace = True를 적어줘야 원본이 수정된다
        # main_good_datas.drop(columns=['title', 'summary_idx', 'article'], inplace=True)  # inplace = True를 적어줘야 원본이 수정된다
        #         print(main_good_datas)
#        google_news_search05.my_save_to_excel("crawl_" + search_word, main_good_datas, t)

    return main_good_datas


def crawl_article(search_word, dateRestrict, search_pages):
    my_api_key = "AIzaSyCeecCL7b4eJbaOmkr0OesT2luBaSN_2tU"  # "귀하의 API 키"
    my_cse_id = "e5d0372b6990e4c20"  # 귀하의 CSE ID "더본솔루션 4.0"
    resource = build("customsearch", 'v1', developerKey=my_api_key).cse()
    my_start = 1
    common_columns = 'summary', 'translate', 'text', 'cos_simil', 'value'
    crawl_columns = 'title', 'link', 'snippet'
    # crawl_columns = crawl_columns + common_columns
    news_columns = 'title', 'media', 'date', 'datetime', 'desc', 'link', 'img'
    # news_columns = news_columns + common_columns

    good_datas = pd.DataFrame(columns=crawl_columns)
    bad_datas = pd.DataFrame(columns = crawl_columns)
    news_df = pd.DataFrame(columns=news_columns)

    count_good_array = 0
    count_bad_array = 0

    # 전체 검색 결과 추정치 얻기//search_word가 공백일 경우 에러난다, 에러처리 필요함
    result = resource.list(q=search_word, cx=my_cse_id, dateRestrict=dateRestrict, filter='1', siteSearchFilter="i",
                           fields='searchInformation').execute()
    total_results = result['searchInformation']['totalResults']
    print("{}에 대한 전체 검색 결과 추정치 : {}".format(search_word, total_results))

    while True:
        try:
            result = resource.list(q=search_word, cx=my_cse_id, filter='1', siteSearchFilter="i", dateRestrict=dateRestrict, start=my_start).execute()
            if 'items' in result:
                for item in result['items']:
                    item_df = pd.DataFrame(data=[[item['title'],item['link'], item['snippet']]], columns=crawl_columns)
                    good_datas = good_datas.append(item_df)
                    good_datas = good_datas.reset_index(drop=True)
            else:
                print("더 이상 결과가 없습니다\n")
                break;

            my_search_num = str(int((my_start+9)/10))
            # print(my_search_num+"페이지 검색 결과입니다\n") 
            if my_start < 90:
                my_start = my_start + 10
            else:
                print("We have reached the allowed limits of Google API\n")
                break
        except:
            print("error")
            break

    print("유효한 검색 결과는 " + str(len(good_datas.index)) + "개입니다\n")
    my_columns = ['title', 'link', 'summary']
    cosine_df = pd.DataFrame(columns=my_columns)
    good_info_df = pd.DataFrame(columns=my_columns)
    return good_datas

def my_google_search(news_df, search_word, search_pages, dateRestrict):
    try:
        googlenews = GoogleNews(period=dateRestrict)
        googlenews.search(search_word)
        result = googlenews.result()
        tmp_df = pd.DataFrame(result)
        for i in range(2, search_pages):
            time.sleep(random.uniform(2, 4))
            googlenews.getpage(i)
            result = googlenews.result()
            tmp_df = pd.DataFrame(result)
            news_df = news_df.append(tmp_df)
            news_df = news_df.reset_index(drop=True)
        return news_df
    except Exception as e:
        print(e)
        pass


def article_download(df):
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    # config = Config()
    # config.browser_user_agent = user_agent
    # config.request_timeout = 10

    list = []
    for ind in df.index:
        dict = {}
        # article = Article(df['link'][ind],config=config)
        article = Article(df['link'][ind])
        try:
            article.download()
            try:
                article.parse()
            #                print("article.parse() succeed")
            except:
                print("article.parse() failed")
            #                return None

            try:
                article.nlp()
            #                print("article.nlp() succeed")
            except:
                print("article.nlp() failed")

            if not article.text:
                # print("dict['text']가 공백이거나 NULL입니다")
                dict['article'] = NaN
            else:
                dict['article'] = article.text
            #                print(dict['article'])

            if not article.summary:
                # print("dict['summary']가 공백이거나 NULL입니다")
                dict['summary'] = NaN
            else:
                dict['summary'] = article.summary
            #                print(dict['summary'])
            list.append(dict)

        except HTTPError as e:
            print('my message : page not found')
        except URLError as e:
            print('my message : The server could not be found!')
        except HTTPError as e:
            print("무슨 에러냐?" + e)
        except newspaper.article.ArticleException as e:
            print("ArticleException")
            print(e)
        else:
            pass

    df = pd.concat([df, pd.DataFrame(list)], axis=1)
    print("article_download 시도 : " + str(len(df.index)) + "개")
    df2 = df.dropna(axis=0)
    print("article_download 성공 : " + str(len(df2.index)) + "개")
    return df2


def article_transfer(df, target_column, col_index):#get_translate함수를 호출해 번역하고 DF를 정리해 주는 함수
    trans_columns = []
    for i in df[target_column]:
        trans_data = google_basic_translate(i, 'ko')
        #        print(trans_data)
        trans_columns.append(trans_data)
    trans_str = target_column + "_tran"
    df.insert(col_index, trans_str, trans_columns, True)


def news_article_download(df):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 10
    list = [] 

    for ind in df.index:
        dict = {}
        article = Article(df['link'][ind], config=config)
        try:
            article.download()
            try:
                article.parse()
                print("article.parse() succeed")
            except:
                print("article.parse() failed")
            #                return None
            article.nlp()
            #            dict['title']=article.title

            if not article.text:
                # print("dict['text']가 공백이거나 NULL입니다")
                dict['article'] = NaN
            else:
                dict['article'] = article.text
            #                print(dict['article'])
            if not article.summary:
                # print("dict['summary']가 공백이거나 NULL입니다")
                dict['summary'] = NaN
            else:
                dict['summary'] = article.summary
            #                print(dict['summary'])
            list.append(dict)

        except HTTPError as e:
            print('my message : page not found')
        except URLError as e:
            print('my message : The server could not be found!')
        except HTTPError as e:
            print("무슨 에러냐?" + e)
        except newspaper.article.ArticleException as e:
            print("ArticleException")
            print(e)
        else:
            pass
    # for i in list:
    #     print(i)

    df_tmp = pd.DataFrame(list)
    result3 = pd.concat([df, df_tmp], axis=1)

    print("article_download finished")
    #    print(df)
    return result3


def my_save_to_excel(search_word, df, t):
    # 파일에 저장

    search_word = search_word.replace('"', '-')

    filename = search_word + " " + str(t.year) + "-" + str(t.month) + "-" + str(t.day) + '.xlsx'

    print(filename)
    mysheetname = "-" + str(t.hour) + "-" + str(t.minute) + "-" + str(t.second)
    excel_writer = StyleFrame.ExcelWriter(filename)
    sf = StyleFrame(df)
    #    sf.set_column_width(columns=['summary', 'translate'], width=70)
    sf.set_row_height(rows=sf.row_indexes, height=100)

    try:
        if df.empty:
            print("df가 비었습니다")
        else:
            print("파일을 저장합니다")
            #            df.to_excel(excel_writer=filename, sheet_name = mysheetname)
            sf.to_excel(excel_writer=excel_writer, sheet_name=mysheetname)
            excel_writer.save()

    except PermissionError:
        input("Close the spreadsheet and press enter.")
        df.to_excel(excel_writer=filename, sheet_name=mysheetname)
        excel_writer.save()

    return df


def init_connect(my_config=Config()):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    #    my_config = Config()
    my_config.browser_user_agent = user_agent
    my_config.request_timeout = 10
    return my_config

# 유료아이디

client_id = "nwjekxmhw3"
client_secret = "6UyUnZQKuMFWYcI7XCTGPOLydyuRyyjr8Jz97D1M"

def google_basic_translate(text, lan):
    translator = Translator()
    translated  = translator.translate(text, dest=lan)

    if translated is not None:
        return translated.text
    else:
        return "번역에 실패했습니다"

def google_adv_translate(text, lan): # 구글 번역    
    client = translate.Client()
    result = client.translate(text, target_language=lan)
    print("구글 번역2입니다")
    return result['translatedText']


def papago_translate(text, lan):  #파파고 번역
    data = {'text': text,
            'source': 'en',
            'target': lan}
    url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
    header = {"X-NCP-APIGW-API-KEY-ID": client_id,
                "X-NCP-APIGW-API-KEY": client_secret}
    
    print("papago_translate를 시작합니다")
    
    response = requests.post(url, headers=header, data=data)
    print("11111111111")
    rescode = response.status_code
    print("22222222222")
    if (rescode == 200):
        send_data = response.json()
        print("333333333")
        trans_data = (send_data['message']['result']['translatedText'])
        print("444444444")
        return trans_data
    else:
        print("Error Code:", rescode)
        return "Sorry. I failed to translate the document."



