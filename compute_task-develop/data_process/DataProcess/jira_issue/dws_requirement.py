import pandas as pd
import datetime


class DwsRequirement(object):
    def __init__(self, db_engine, dws_table_name, requirement_history_sql, mysql_helper):
        self.db_engine = db_engine
        self.dws_table_name = dws_table_name
        self.requirement_history_sql = requirement_history_sql
        self.mysql_helper = mysql_helper

    def fun(self, x):
        if x[x["to_string"] == "Verify"]["event_time"].count() == 0:
            return x.iloc[0]
        if x[x["to_string"] == "Solution"]["event_time"].count() == 0:
            return x.iloc[0]
        delta = x[x["to_string"] == "Verify"]["event_time"].to_list()[-1] - \
                x[x["to_string"] == "Solution"]["event_time"].to_list()[0]
        x['verify_cost'] = delta.days * 24 + delta.seconds / 3600
        if x[x["to_string"] == "Complete"]["event_time"].count() == 0:
            return x.iloc[0]
        delta = x[x["to_string"] == "Complete"]["event_time"].to_list()[-1] - \
                x[x["to_string"] == "Verify"]["event_time"].to_list()[-1]
        x['complete_cost'] = delta.days * 24 + delta.seconds / 3600
        return x.iloc[0]

    def write_data(self):
        df = pd.read_sql(self.requirement_history_sql, con=self.db_engine)
        df['verify_cost'] = pd.NaT
        df['complete_cost'] = pd.NaT
        df = df.groupby(["vdr", "srms"], as_index=False).apply(self.fun)
        df = df.loc[:, ["vdr", "vdr_status", "srms", "srms_status", "team", "planned_bp", "verify_cost", "complete_cost", "ctask", "ctask_status", "qtask", "qtask_status"]]
        df.insert(loc=0, column="update_datetime", value=datetime.datetime.now())
        df.to_sql(self.dws_table_name, con=self.db_engine, if_exists="append", index=False, method=self.mysql_helper.insert_on_duplicate)
