import time
from apscheduler.schedulers.blocking import BlockingScheduler
from DataProcess import settings
from DataProcess.jira_issue.ads_vdr import AdsVdr
from DataProcess.jira_issue.compute_vdr import ComputeVdr
from DataProcess.jira_issue.dws_vdr import DwsVdr
from DataProcess.jira_issue.dws_requirement import DwsRequirement
from DataProcess.jira_issue.ads_requirement import AdsRequirement
from DataProcess.settings import MYSQL_ONLINE_CONFIG


def vdr_task():
    issue_dict = {}
    vdr_list = []
    print('current running task time ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    compute_vdr = ComputeVdr(MYSQL_ONLINE_CONFIG['host'],
                             MYSQL_ONLINE_CONFIG['username'],
                             MYSQL_ONLINE_CONFIG['password'],
                             MYSQL_ONLINE_CONFIG['database'],
                             MYSQL_ONLINE_CONFIG['charset'],
                             MYSQL_ONLINE_CONFIG['port'],
                             settings.SRMS_EDMS_SQL,
                             settings.VDR_SQL,
                             issue_dict,
                             vdr_list)#连接tidb

    compute_vdr.get_issue_info()
    compute_vdr.compute_vdr()

    dws_vdr = DwsVdr(settings.DB_ENGINE,
                     settings.DWS_DEVELOP_JIRA_VDR_TABLE_NAME,
                     settings.DWS_DEVELOP_JIRA_VDR_TABLE_COLUMNS,
                     vdr_list,
                     compute_vdr.mysql_helper)
    dws_vdr.write_data()

    ads_vdr = AdsVdr(settings.DB_ENGINE,
                     settings.DWS_DEVELOP_JIRA_VDR_TABLE_NAME,
                     settings.ADS_DEVELOP_JIRA_VDR_TABLE_NAME,
                     compute_vdr.mysql_helper)
    ads_vdr.write_data()

    dws_requirement = DwsRequirement(settings.DB_ENGINE,
                                     settings.DWS_DEVELOP_REQUIREMENT_COST_TIME_TABLE_NAME,
                                     settings.REQUIREMENTS_HISTORY_SQL,
                                     compute_vdr.mysql_helper)
    dws_requirement.write_data()

    ads_requirement = AdsRequirement(settings.DB_ENGINE,
                                     settings.DWS_DEVELOP_REQUIREMENT_COST_TIME_TABLE_NAME,
                                     settings.ADS_DEVELOP_REQUIREMENT_COST_TIME_TABLE_NAME,
                                     compute_vdr.mysql_helper)
    ads_requirement.write_data()


if __name__ == '__main__':
    # blocking_scheduler = BlockingScheduler(executors=settings.APSCHEDULER_EXECUTORS,
    #                                        job_defaults=settings.APSCHEDULER_JOB_DEFAULTS)
    # # 每天凌晨3点执行定时任务
    # blocking_scheduler.add_job(vdr_task, trigger="cron", hour='3', timezone='Asia/Shanghai')
    # # 仅用于测试, 每3分钟执行一次定时任务
    # # blocking_scheduler.add_job(vdr_task, trigger="cron", minute='*/3', timezone='Asia/Shanghai')
    # blocking_scheduler.start()
    AdsRequirement(object)
    object.vdr_count()
