import pandas as pd
import datetime
from datetime import timedelta
import sys
sys.path.append("../utils")
from mysql_helper import MysqlHelper

class AdsVdr(object):
    def __init__(self, db_engine, dws_table_name, ads_table_name, mysql_helper):
        self.db_engine = db_engine
        self.dws_table_name = dws_table_name
        self.ads_table_name = ads_table_name
        self.mysql_helper = mysql_helper

    def write_data(self):
        result = "select * from " + self.dws_table_name
        df = pd.read_sql(result, con=self.db_engine)
        # 过滤掉VDR不在状态Discard
        df = df[(df['vdr_status'] != 'Discard')]
        # 将VDR去重计数
        df_vdr_0 = df.groupby(by=['planned_bp', 'vdr']).size().groupby('planned_bp').size()
        # 过滤掉VDR不在状态Open Discard
        df = df[(df['vdr_status'] != 'Discard') & (df['vdr_status'] != 'Open')]
        # 求得VDR数， 一个指标的分母
        df_vdr = df.groupby(by=['planned_bp', 'vdr']).size().groupby('planned_bp').size()
        # 过滤出满足srms状态的， 其他几个指标的分母是这个条件的
        df = df[(df["srms_status"] == "Solution") | (df["srms_status"] == "Verify") | (
                    df["srms_status"] == "Feature Missing") | (df["srms_status"] == "Complete")]

        # 一个VDR关联多个SMRS情况：
        # 取“交集”， 即-几个srms同时满足条件，指标记为真
        # bug相关的两个指标，需要取“并集”， 即几个srms中有一个关联了Bug，就计数
        df_max = df.groupby(by='vdr').max()
        df_max = df_max.groupby(by='planned_bp').sum(numeric_only=True)
        df = df.groupby(by='vdr').min()
        df = df.groupby(by='planned_bp').sum(numeric_only=True)
        df['critical_srms_bug'] = df_max['critical_srms_bug']
        df['critical_edms_bug'] = df_max['critical_edms_bug']
        df.drop('id', axis=1, inplace=True)
        df.insert(loc=0, column='vdr', value=df_vdr)
        df.insert(loc=0, column='vdr_0', value=df_vdr_0)
        df.insert(loc=0, column='planned_bp', value=df.index)
        df.insert(loc=0, column="update_datetime", value=datetime.datetime.now())
        df.insert(loc=0, column="event_time", value=(datetime.datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))

        # 百分比指标
        df['handshake_rate'] = round(df['vdr'] / df['vdr_0'], 3)
        df['disassemble_rate'] = round(df['disassemble'] / df['vdr'], 3)
        df['implement_rate'] = round(df['implement'] / df['disassemble'], 3)
        df['ctask_done_rate'] = round(df['ctask_done'] / df['disassemble'], 3)
        df['qtask_done_rate'] = round(df['qtask_done'] / df['disassemble'], 3)
        df['no_critical_srms_bug_rate'] = 1 - round(df['critical_srms_bug'] / df['disassemble'], 3)
        df['no_critical_edms_bug_rate'] = 1 - round(df['critical_edms_bug'] / df['disassemble'], 3)
        # 入库
        print(df)
        df.to_sql(self.ads_table_name, con=self.db_engine, if_exists="append", index=False, method=self.mysql_helper.insert_on_duplicate)


