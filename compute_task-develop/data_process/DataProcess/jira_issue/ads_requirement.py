import pandas as pd
import numpy as np
import datetime
from datetime import timedelta


class AdsRequirement(object):
    def __init__(self, db_engine, dws_table_name, ads_table_name, mysql_helper):
        self.db_engine = db_engine
        self.dws_table_name = dws_table_name
        self.ads_table_name = ads_table_name
        self.mysql_helper = mysql_helper

    def vdr_count(self, group):
        size = len(group.groupby("vdr").size())
        return size

    def vdr_handshake(self, group):
        group = group[["vdr", "vdr_status"]]
        group["vdr_handshake_flag"] = np.where(group["vdr_status"] != "Open", 1, 0)
        group = group.groupby("vdr")["vdr_handshake_flag"].min()
        return group.sum()
    def vdr_disassemble(self, group):
        group = group[["vdr", "srms_status"]]
        group["srms_disassemble_flag"] = np.where((group["srms_status"] == "Complete") |
                                                  (group["srms_status"] == "Verify") |
                                                  (group["srms_status"] == "Solution") |
                                                  (group["srms_status"] == "Feature Missing"),
                                                  1, 0)
        group = group.groupby("vdr")["srms_disassemble_flag"].min()
        return group.sum()

    def vdr_verify(self, group):
        group = group[["vdr", "srms_status"]]
        group["srms_verify_flag"] = np.where(group["srms_status"] == "Verify", 1, 0)
        group = group.groupby("vdr")["srms_verify_flag"].min()
        return group.sum()

    def vdr_complete(self, group):
        group = group[["vdr", "srms_status"]]
        group["srms_complete_flag"] = np.where(group["srms_status"] == "Complete", 1, 0)
        group = group.groupby("vdr")["srms_complete_flag"].min()
        return group.sum()

    def vdr_implement(self, group):
        group = group[["vdr", "srms_status"]]
        group["srms_implement_flag"] = np.where((group["srms_status"] == "Complete") | (group["srms_status"] == "Verify"), 1, 0)
        group = group.groupby("vdr")["srms_implement_flag"].min()
        return group.sum()

    def ctask_done(self, group):
        group = group[["vdr", "ctask_status"]]
        group["ctask_done_flag"] = np.where(group["ctask_status"] == "Done", 1, 0)
        group = group.groupby("vdr")["ctask_done_flag"].min()
        return group.sum()

    def qtask_done(self, group):
        group = group[["vdr", "qtask_status"]]
        group["qtask_done_flag"] = np.where(group["qtask_status"] == "Done", 1, 0)
        group = group.groupby("vdr")["qtask_done_flag"].min()
        return group.sum()

    def write_data(self):
        result = "select * from " + self.dws_table_name
        df = pd.read_sql(result, con=self.db_engine)

        # 过滤掉VDR不在状态Discard
        df = df[(df['vdr_status'] != 'Discard')]

        series_vdr_count = df.groupby(["planned_bp", "team"]).apply(self.vdr_count)
        series_vdr_count.name = "vdr"

        series_vdr_handshake = df.groupby(["planned_bp", "team"]).apply(self.vdr_handshake)
        series_vdr_handshake.name = "vdr_handshake"

        series_vdr_disassemble = df.groupby(["planned_bp", "team"]).apply(self.vdr_disassemble)
        series_vdr_disassemble.name = "vdr_disassemble"

        series_vdr_verify = df.groupby(["planned_bp", "team"]).apply(self.vdr_verify)
        series_vdr_verify.name = "vdr_verify"
        series_vdr_complete = df.groupby(["planned_bp", "team"]).apply(self.vdr_complete)
        series_vdr_complete.name = "vdr_complete"
        series_vdr_implement = df.groupby(["planned_bp", "team"]).apply(self.vdr_implement)
        series_vdr_implement.name = "vdr_implement"

        series_ctask_done = df.groupby(["planned_bp", "team"]).apply(self.ctask_done)
        series_ctask_done.name = "ctask_done"
        series_qtask_done = df.groupby(["planned_bp", "team"]).apply(self.qtask_done)
        series_qtask_done.name = "qtask_done"

        df = df.pivot_table(values=["verify_cost", "complete_cost"], index=["planned_bp", "team"],
                            aggfunc={'verify_cost': np.mean, 'complete_cost': np.mean})
        df = pd.concat([df,
                        series_vdr_count,
                        series_vdr_handshake,
                        series_vdr_disassemble,
                        series_vdr_verify,
                        series_vdr_complete,
                        series_vdr_implement,
                        series_ctask_done,
                        series_qtask_done],
                       axis='columns')
        df = df.reset_index()
        df["verify_cost"] = round(df["verify_cost"], 1)
        df["complete_cost"] = round(df["complete_cost"], 1)
        df["handshake_rate"] = round(df["vdr_handshake"] / df["vdr"], 3)
        df["disassemble_rate"] = round(df["vdr_disassemble"] / df["vdr_handshake"], 3)
        df["implement_rate"] = round(df["vdr_implement"] / df["vdr_disassemble"], 3)
        df["ctask_done_rate"] = round(df["ctask_done"] / df["vdr_disassemble"], 3)
        df["qtask_done_rate"] = round(df["qtask_done"] / df["vdr_disassemble"], 3)

        df.insert(loc=0, column="update_datetime", value=datetime.datetime.now())
        df.insert(loc=0, column="event_time", value=(datetime.datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))

        df.to_sql(self.ads_table_name, con=self.db_engine, if_exists="append", index=False, method=self.mysql_helper.insert_on_duplicate)

