import datetime
import pandas as pd
import sys
sys.path.append("../utils")
from mysql_helper import MysqlHelper

class DwsVdr(object):
    def __init__(self, db_engine, dws_table_name, table_columns, vdr_list, mysql_helper):
        self.vdr_list = vdr_list
        self.db_engine = db_engine
        self.dws_table_name = dws_table_name
        self.table_columns = table_columns
        self.mysql_helper = mysql_helper

    def write_data(self):
        df = pd.DataFrame(self.vdr_list, columns=self.table_columns)
        df.sort_values(by="vdr", inplace=True)
        df["disassemble"] = (df["srms_status"] == "Solution") | (df["srms_status"] == "Verify") | (
                    df["srms_status"] == "Feature Missing") | (df["srms_status"] == "Complete")
        df["implement"] = (df["srms_status"] == "Verify") | (df["srms_status"] == "Complete")
        df["ctask_done"] = df["ctask_status"] == "Done"
        df["qtask_done"] = df["qtask_status"] == "Done"
        df["critical_srms_bug"] = df["srms_bug"] != ""
        df["critical_edms_bug"] = df["edms_bug"] != ""
        df.insert(loc=0, column="update_datetime", value=datetime.datetime.now())
        df.to_sql(self.dws_table_name, con=self.db_engine, if_exists="append", index=False, method=self.mysql_helper.insert_on_duplicate)

