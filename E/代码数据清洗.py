import numpy as np
import pymysql.cursors
from dbutils.pooled_db import PooledDB
import pandas as pd
import re

Pool = PooledDB(pymysql,
                mincached=2,
                maxcached=5,
                host='10.132.166.89',
                port=4000,
                user='rw_nio',
                passwd='F7taJfkU%X',
                database='sync_data',
                cursorclass=pymysql.cursors.DictCursor)


def fun_get_user(sql, col=None):
    conn = Pool.connection()
    with conn.cursor() as mycursor:
        mycursor.execute(sql)
        column_names = [i[0] for i in mycursor.description]  ##表名
        group = mycursor.fetchall()
        group = pd.DataFrame(group, columns=column_names)
        if col is not None:
            group[col] = group[col].apply(lambda x: x.strftime("%Y-%m-%d"))

    return group


def pattern_match(str):
    list = []
    type = ['NT1VDR','CDCFE','NT2EDMS','AIS','EDMS','NT2VDR','SRMS']###jira库中的票型
    for pattern in type:
        while re.search(pattern, str):
            if pattern=='NT2EDMS':
                type.remove('EDMS')
            list = re.findall(r"%s-+[0-9]+"%(pattern), str)
            break
    return list


def data_handle(df,tile):
    output = []
    for str in range(len(df)):
        data = df[tile]
        group = pattern_match(data.iloc[str])
        group = ','.join(group)
        output.append(group)
    df['issue_key'] = pd.DataFrame(output)
    return df


def split_table(df,label):
    # 一、把“商品”字段拆分，分为多列
    df_tmp = df['issue_key'].str.split(',', expand=True)

    # 二、将行索引转变成列索引(第二层)，得到一个层次化的Series
    df_tmp = df_tmp.stack()

    # 三、重置索引，并删除多于的索引
    df_tmp = df_tmp.reset_index(level=1, drop=True)

    # 四、与原始数据合并
    df_tmp.name = label
    df_new = git_df.drop([label], axis=1).join(df_tmp).reset_index().drop(columns='index')

    return df_new


if __name__ == '__main__':
    gerrit_sql = '''
    SELECT subject FROM ods_develop_gerrit_commits_1d_i
    '''
    git_sql = '''
    SELECT author_email,date(commit_time) commit_time,replace(namespace,' ','') namespace,title 
    FROM ods_develop_git_commits_1d_i
    '''

    # gerrit_df = fun_get_user(gerrit_sql)
    # gerrit_df = data_handle(gerrit_df,'subject')
    # print(gerrit_df)

    git_df = fun_get_user(git_sql)
    git_df = data_handle(git_df,'title')

    df_new = split_table(git_df,'issue_key')
    # print(df_new)


    jira_sql = '''
    SELECT issue_key,baseline,component,team,priority,summary,process_status,
                                (case when summary LIKE '%离车不下电%' then '离车不下电' 
                        when summary LIKE '%宠物%' then '宠物模式'
                        when summary LIKE '%露营%' then '露营模式' ELSE NULL END) tag,
                                date(issue_create) issue_create
    FROM ods_develop_jira_issue_infos_1d_i
    WHERE team = 'Underground(DC车控)'
    AND summary LIKE '%离车不下电%' OR summary LIKE '%宠物%' OR summary LIKE '%露营%' 
    '''
    jira_df = fun_get_user(jira_sql)

    df_new  = pd.merge(df_new,jira_df,'inner','issue_key')

    print(df_new)





