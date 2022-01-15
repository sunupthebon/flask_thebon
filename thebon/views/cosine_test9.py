import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import linear_kernel

# import google_news_search05
from datetime import datetime
import os
from newspaper import Article


#my_cosine_similarity3는 구글 뉴스기사(x_list)와 비교, my_cosine_similarity는 크롤링 데이터간 비교

def my_cosine_similarity3(x_list, y_df, target_coloumn):
    tmp_y_df = pd.DataFrame(y_df)

    # 첫 행에  비교 기사 추가
    tmp_y_df.loc[-1] = x_list
    tmp_y_df.index = tmp_y_df.index + 1  # shifting index
    tmp_y_df = tmp_y_df.sort_index()  # sorting by index

    tmp_y_df[target_coloumn] = [str(item) for item in tmp_y_df[target_coloumn]]  # none 값 없애기
    tfidf_vect_simple = TfidfVectorizer(stop_words=["and", "is", "the", "this"])
    feature_vect_simple = tfidf_vect_simple.fit_transform(tmp_y_df[target_coloumn])
    j = 0
    tmp_coloumns = []

    # 비교 기사를 cos_simil 오른쪽에 배치
    #    crawl_df = pd.DataFrame(columns = ['target_title', 'target_link', 'target_summary'])
    target_title_coloumns = []
    target_link_coloumns = []
    target_summary_coloumns = []

    for tmp_feature_vect_simple in feature_vect_simple:
        similarity_simple = cosine_similarity(feature_vect_simple[0], tmp_feature_vect_simple)
        tmp_coloumns.append(similarity_simple)

        target_title_coloumns.append(x_list['title'])
        target_link_coloumns.append(x_list['link'])
        target_summary_coloumns.append(x_list['summary'])

        j = j + 1

    # 3번째 컬럼에 cos_simil 추가
    tmp_y_df.insert(3, "cos_simil", tmp_coloumns, True)

    tmp_y_df.insert(4, "target_title", target_title_coloumns, True)
    tmp_y_df.insert(5, "target_link", target_link_coloumns, True)
    tmp_y_df.insert(6, "target_summary", target_summary_coloumns, True)

    # 첫행에 있는 비교 기사 삭제
    tmp_y_df = tmp_y_df.drop(0, axis=0)
    tmp_y_df.index = tmp_y_df.index - 1  # shifting index

    #    print(tmp_y_df)

    return tmp_y_df


def my_cosine_similarity(y_df, target_coloumn):  # y_df를 인자로 받아서 target_coloumn의 유사도를 구하고 유사도가 높은 행을 제거해 반환한다

    tfidf_vect_simple = TfidfVectorizer(stop_words=["and", "is", "the", "this"])
    feature_vect_simple = tfidf_vect_simple.fit_transform(
        y_df[target_coloumn].values.astype('U'))  ## Even astype(str) would work
    print(feature_vect_simple.shape)
    cosine_matrix = cosine_similarity(feature_vect_simple, feature_vect_simple)
    cos_idx = [True] * feature_vect_simple.shape[0]
    for j, idx in enumerate(cosine_matrix):
        if cos_idx[j] == True:
            for i, sub_idx in enumerate(idx):
                if j < i and cos_idx[i] == True:
                    if sub_idx > 0.2:
                        cos_idx[i] = False
    # cos_idx 리스트를 y_df에 summary_idx란 컬럼으로 붙이고 cos_idx가 False인 행을 삭제한다

    y_df.insert(3, "summary_idx", cos_idx, True)
    return y_df.drop(y_df[y_df['summary_idx'] == False].index).reset_index(drop=True)


if __name__ == "__main__":
    while True:
        print("파일 df와 비교 완료")
        break;






