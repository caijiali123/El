from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

MYSQL_ONLINE_CONFIG = {
    "host": "10.132.166.89",
    'port': 4000,
    'username': 'rw_nio',
    'password': 'F7taJfkU%X',
    'database': 'sync_data',
    'charset': 'utf8'
}

MYSQL_TEST_CONFIG = {
    "host": "10.132.119.48",
    'port': 4000,
    'username': 'nio_rd',
    'password': '8ja^C5wjcL',
    'database': 'develop_test',
    'charset': 'utf8'
}

DB_ENGINE = f'mysql+pymysql://{MYSQL_ONLINE_CONFIG["username"]}:' \
         f'{MYSQL_ONLINE_CONFIG["password"]}@{MYSQL_ONLINE_CONFIG["host"]}' \
         f':{MYSQL_ONLINE_CONFIG["port"]}/{MYSQL_ONLINE_CONFIG["database"]}'

VDR_SQL = r"SELECT issue_key, issue_links, subtasks, process_status, component, planed_bp, team FROM sync_data.ods_develop_jira_issue_infos_1d_i WHERE project = 'NT1VDR' AND (planed_bp like 'BL3.%' OR planed_bp like 'Alder1.%') AND component like '%CDC%'"
SRMS_EDMS_SQL = r"SELECT issue_key, team, process_status, issue_links, subtasks, issue_type, priority FROM sync_data.ods_develop_jira_issue_infos_1d_i WHERE project = 'SRMS' OR project='EDMS'"
REQUIREMENTS_HISTORY_SQL=r"SELECT vdr, vdr_status, srms, srms_status, team, planned_bp, ctask, ctask_status, qtask, qtask_status, H.from_string, H.to_string, H.event_time FROM dws_develop_jira_vdr_srms_info_1d_i LEFT JOIN ods_develop_jira_issue_histories_1d_i AS H ON dws_develop_jira_vdr_srms_info_1d_i.srms = H.issue_key ORDER BY planned_bp,srms, event_time;"

DWS_DEVELOP_JIRA_VDR_TABLE_NAME = "dws_develop_jira_vdr_srms_info_1d_i"
ADS_DEVELOP_JIRA_VDR_TABLE_NAME = "ads_develop_jira_vdr_srms_info_1d_a"
DWS_DEVELOP_REQUIREMENT_COST_TIME_TABLE_NAME = "dws_develop_requirement_cost_time_info_1d_a"
ADS_DEVELOP_REQUIREMENT_COST_TIME_TABLE_NAME = "ads_develop_requirement_cost_time_info_1d_i"
DWS_DEVELOP_JIRA_VDR_TABLE_COLUMNS = ["vdr", "vdr_status", "planned_bp", "srms", "srms_status", "srms_type", "team", "ctask",
                                      "ctask_status", "qtask", "qtask_status", "srms_bug", "edms_bug"]

# apscheduler执行器配置
APSCHEDULER_EXECUTORS = {
    'default': ThreadPoolExecutor(10),
    'processpool': ProcessPoolExecutor(3)
}

# apscheduler作业数配置
APSCHEDULER_JOB_DEFAULTS = {
    'coalesce': False,
    'max_instances': 3
}
