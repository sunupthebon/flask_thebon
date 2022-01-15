from flask import Blueprint, render_template, g, request
from pandas.core.dtypes.missing import notnull
from thebon.models import User, User_data, Crawling
from thebon.views import myfunction
from thebon.views.auth_views import login_required
import sqlite3
import time
import pandas as pd

bp = Blueprint('crawling', __name__, url_prefix='/crawling')

@bp.route('/search/')
@login_required
def search_list():
    my_search_list = User_data.query.filter_by(user_id = g.user.id).all()
    return render_template('crawling/search_word.html', search_list=my_search_list)

# @bp.route('/crawling_list/')#크롤링 결과를 보여주는 화면
# @login_required
# def crawling_list(crawling_df):
#     # return render_template('crawling/crawling_list.html', crawling_df=crawling_df)
#     return render_template('test.html', crawling_df=crawling_df)

@bp.route('/sunup/<int:user_id>')
@login_required
def sunup(user_id):
    my_num = g.user.id
    my_search_list = User_data.query.order_by(User_data.search_word)
    return render_template('crawling/search_word.html', search_list=my_search_list)

@bp.route('/list/')
@login_required
def _list():
    my_crawling_list = Crawling.query.order_by(Crawling.create_date.desc())
    return render_template('crawling/crawling_list.html', crawling_list=my_crawling_list)

@bp.route('/detail/<int:crawling_id>/')
@login_required
def detail(crawling_id):
    crawling = Crawling.query.get_or_404(crawling_id)
    return render_template('crawling/crawling_detail.html', crawling=crawling)

@bp.route('/submit/')
@login_required
def submit():
    form = SubmitForm()
    return render_template('crawling/submit_form.html', form=form)

@bp.route('/updatedb/', methods=['POST','GET'])
@login_required
def updatedb():
    start = time.time()  # 시작 시간 저장
    # if request.method == 'POST':
    tmp_my_search_list = []
    data = request.form

    for i in data.items():  # items() method is used to return the list with all dictionary keys with values.
        tmp = i.__getitem__(1)
        tmp = tmp.strip()
        tmp_my_search_list.append(tmp)

    # 중복 검색어, 공백 검색어 제거
    my_search_list = list(dict.fromkeys(tmp_my_search_list))
    my_search_list = list(filter(None, my_search_list))
    print(my_search_list)

    # deleteRecord(g.user.id)
    updateRecord(g.user.id, my_search_list)
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
    return search_list()

@bp.route('/solo_search/', methods=['POST','GET'])
@login_required
def solo_search():
    start = time.time()  # 시작 시간 저장
    data = request.form
    search_word = request.form['solo_name']
    # result_df = myfunction.crawling_main_fun(search_word)
    large_dic = {}
    large_dic[search_word] = myfunction.crawling_main_fun(search_word)
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
    return render_template('crawling/crawling_list.html', large_dic=large_dic)
    # return render_template('crawling/crawling_list.html', crawling_df=result_df, search_word=search_word)

@bp.route('/multi_search/', methods=['POST','GET'])
@login_required
def multi_search():
    start = time.time()  # 시작 시간 저장
    tmp_my_search_list = []
    data = request.form
    result_df = pd.DataFrame

    for i in data.items():  # items() method is used to return the list with all dictionary keys with values.
        tmp = i.__getitem__(1)
        # tmp = tmp.strip()
        tmp_my_search_list.append(tmp)

    # 중복 검색어, 공백 검색어 제거
    my_search_list = list(dict.fromkeys(tmp_my_search_list))
    my_search_list = list(filter(None, my_search_list))
    print(my_search_list)

    #딕셔너리 이용하기
    large_dic = {}
    for search_word in my_search_list:
        large_dic[search_word] = myfunction.crawling_main_fun(search_word)
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
    return render_template('crawling/crawling_list.html', large_dic=large_dic)

def updateRecord(user_id, my_search_list):
    try:
        sqliteConnection = sqlite3.connect('thebon.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite for updateRecord")
        sql_delete_query = 'DELETE from User_data where user_id = '+str(user_id)
        cursor.execute(sql_delete_query)
        for searchword in my_search_list:
            searchword = "'" + searchword + "'"
            sql_insert_query = 'insert into User_data(user_id, search_word) values(' + '1' + ', ' + searchword + ')'
            print(sql_insert_query)
            cursor.execute(sql_insert_query)
        sqliteConnection.commit()
        print("Record updated successfully ")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


# @bp.route('/more_info/')
# @login_required
# def more_info():
#     print("aaaaaaaaaaaaaaaaa")
#     if request.method == 'GET':
#         tmp_my_search_list = []
#         data = request.form
#         print(data)

@bp.route('/more_info/', methods=['POST','GET'])
@login_required
def more_info():
    start = time.time()  # 시작 시간 저장
    target_url = request.form['art_url']
    print(target_url)
    print("time spent : ", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
    sum_origin, sum_trans = myfunction.more_info(target_url)
    return render_template('crawling/sum_popup.html', sum_origin=sum_origin, sum_trans=sum_trans)
    