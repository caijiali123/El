import numpy as np
import pymysql.cursors
from dbutils.pooled_db import PooledDB
import pandas as pd
import json
import datetime
import matplotlib.pyplot as plt

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

if __name__ == '__main__':
    sql_developer = '''
    SELECT team,post_year,post_week,num feedback_num,dist_num,t3.department,function_num,loc_add_line,dev_equivalent
    FROM
    (SELECT (case when department IN ('导航应用团队','地图引擎团队') then '导航应用/地图引擎团队' ELSE department END ) department,
    YEAR(date) time_year,week(date) time_week,
    sum(function_num) function_num,sum(loc_add_line) loc_add_line,sum(dev_equivalent) dev_equivalent
    FROM
    (select email,third_department_name,fourth_department_name,
    (case when LENGTH(fourth_department_name)=0 THEN third_department_name ELSE fourth_department_name END ) department
    
    from sync_data.ods_meta_people_info
    where second_department_id = 'od-b3e33b4dad27b7e6124fbfff2b786d3e') t
    LEFT JOIN
    (SELECT DISTINCT primary_email,date,
                    round(sum(function_num)/count(DISTINCT developer_name),2) function_num,
                    round(sum(loc_add_line)/count(DISTINCT developer_name),2) loc_add_line,
                    round(sum(dev_equivalent)/count(DISTINCT developer_name),2) dev_equivalent
    FROM
    sync_data.ads_merico_developer_efficiency_metric_1w_a 
    GROUP BY primary_email,date
    ) t1
    ON t.email=t1.primary_email
    WHERE LENGTH(date)>0
    GROUP BY (case when department IN ('导航应用团队','地图引擎团队') then '导航应用/地图引擎团队' ELSE department END ),YEAR(date) ,week(date) 
    )t2 
    RIGHT JOIN
    (SELECT *,
    (case when team IN ('系统战队','账号') then '系统团队'
                when team IN ('三方应用战队','FOTA') then '系统工程团队'
                when team IN ('Vision1','Vision2','Happy Driving 安心驾驶') then '数字座舱平台1团队'
                when team IN ('导航EU','导航CN') then '导航应用/地图引擎团队'
                when team IN ('媒体娱乐') then '媒体团队'
                when team IN ('NOMI') then '智能客户端开发团队'
                when team IN ('多模') then '多模交互实验室'
                when team IN ('COE非战队','稳定性战队') then '操作系统团队'
                when team IN ('海外应用战队') then '海外团队'
                when team IN ('Underground(DC车控)') then '车控团队'
                when team IN ('XR') then '座舱软件架构与中台部'
                ELSE NULL END
    ) department
    FROM
    (
    SELECT team,year(post_timestamp) post_year,week(post_timestamp) post_week,count(vin) num,count(DISTINCT vin) dist_num
    FROM ods_user_feedback_voice_and_req_1d_a
    WHERE LENGTH(team)>0
    AND domain = 'DC'
    GROUP BY team,year(post_timestamp),week(post_timestamp) 
    ) t
    ) t3
    ON t2.department = t3.department AND t2.time_year = t3.post_year AND t2.time_week = t3.post_week

    '''
    df = fun_get_user(sql_developer).astype(str)

    df['event_time'] = df[['post_year','post_week']].apply(lambda x: "-".join(x),axis=1)

    data = df[['department', 'event_time', 'feedback_num', 'dev_equivalent']]

    for index,group in data.groupby(['department']):
        plt.title(index)
        plt.plot(group['event_time'].sort_values(ascending=True), group['feedback_num'])
        plt.plot(group['event_time'].sort_values(ascending=True), group['dev_equivalent'])
        print(plt.show())


