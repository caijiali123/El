DROP TABLE IF EXISTS `dws_develop_jira_vdr_srms_info_1d_i`;
CREATE TABLE `dws_develop_jira_vdr_srms_info_1d_i` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `vdr` varchar(32) DEFAULT NULL COMMENT '需求故事号码',
    `vdr_status` varchar(32) DEFAULT NULL COMMENT '需求故事的状态',
    `planned_bp` varchar(32) DEFAULT NULL COMMENT '平台版本',
    `srms` varchar(32) DEFAULT NULL COMMENT '需求号码',
    `srms_status` varchar(32) DEFAULT NULL COMMENT '需求状态',
    `srms_type` varchar(32) DEFAULT NULL COMMENT '需求类型',
    `team` varchar(32) DEFAULT NULL COMMENT '需求所属战队',
    `ctask` varchar(32) DEFAULT NULL COMMENT '测试用例号码',
    `ctask_status` varchar(32) DEFAULT NULL COMMENT '测试用例状态',
    `qtask` varchar(32) DEFAULT NULL COMMENT '测试号码',
    `qtask_status` varchar(32) DEFAULT NULL COMMENT '测试状态',
    `srms_bug` varchar(255) DEFAULT NULL COMMENT '需求关联的智能座舱bug值',
    `edms_bug` varchar(255) DEFAULT NULL COMMENT '需求关联的整车bug值',
    `disassemble` tinyint(1) DEFAULT NULL COMMENT '需求故事是否已经拆解',
    `implement` tinyint(1) DEFAULT NULL COMMENT '需求故事是否已经实现',
    `ctask_done` tinyint(1) DEFAULT NULL COMMENT '测试用例是否完成',
    `qtask_done` tinyint(1) DEFAULT NULL COMMENT '测试是否完成',
    `critical_srms_bug` tinyint(1) DEFAULT NULL COMMENT '是否有P0的智能座舱的Bug',
    `critical_edms_bug` tinyint(1) DEFAULT NULL COMMENT '是否有P0的整车的Bug',
    `create_datetime` datetime DEFAULT now() COMMENT '创建日期',
    `update_datetime` datetime DEFAULT now() COMMENT '更新日期',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1;
ALTER TABLE `dws_develop_jira_vdr_srms_info_1d_i` ADD UNIQUE INDEX `uniq_vdr_srms` (`vdr`, `srms`) USING BTREE;
SET FOREIGN_KEY_CHECKS = 1;

DROP TABLE IF EXISTS `ads_develop_jira_vdr_srms_info_new_1d_a`;
CREATE TABLE `ads_develop_jira_vdr_srms_info_new_1d_a` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `planned_bp` varchar(32) DEFAULT NULL COMMENT '平台版本',
    `vdr_0` bigint(20) DEFAULT NULL COMMENT '当前版本不在Discard状态的VDR Story数',
    `vdr` bigint(20) DEFAULT NULL  COMMENT '当前版本不在Open或Discard状态的VDR Story数',
    `disassemble` bigint(20) DEFAULT NULL COMMENT '已拆解VDR Story数',
    `implement` bigint(20) DEFAULT NULL COMMENT '已实现VDR Story数',
    `ctask_done` bigint(20) DEFAULT NULL COMMENT '测试用例已完成的VDR Story数',
    `qtask_done` bigint(20) DEFAULT NULL COMMENT '测试已完成的VDR Story数',
    `critical_srms_bug` bigint(20) DEFAULT NULL COMMENT '关联P0 SMRSbug的VDR Story数',
    `critical_edms_bug` bigint(20) DEFAULT NULL COMMENT '关联P0 EDMSbug的VDR Story数',
    `handshake_rate` double DEFAULT NULL COMMENT '需求握手率',
    `disassemble_rate` double DEFAULT NULL COMMENT '需求拆解率',
    `implement_rate` double DEFAULT NULL COMMENT '需求实现率',
    `ctask_done_rate` double DEFAULT NULL COMMENT '针对需求的测试用例覆盖率',
    `qtask_done_rate` double DEFAULT NULL COMMENT '针对需求的测试覆盖率',
    `no_critical_srms_bug_rate` double DEFAULT NULL COMMENT '提测SQE一次通过率',
    `no_critical_edms_bug_rate` double DEFAULT NULL COMMENT '提测DIO一次通过率',
    `event_time` varchar(64) DEFAULT NULL COMMENT '事件日期',
    `create_datetime` datetime DEFAULT now() COMMENT '创建日期',
    `update_datetime` datetime DEFAULT now() COMMENT '更新日期',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1;
ALTER TABLE `ads_develop_jira_vdr_srms_info_new_1d_a` ADD UNIQUE INDEX `uniq_planned_bp_event_time` (`planned_bp`, `event_time`) USING BTREE;
SET FOREIGN_KEY_CHECKS = 1;

DROP TABLE IF EXISTS `dws_develop_requirement_cost_time_info_1d_a`;
CREATE TABLE `dws_develop_requirement_cost_time_info_1d_a` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `vdr` varchar(32) DEFAULT NULL COMMENT '需求故事号码',
  `vdr_status` varchar(32) DEFAULT NULL COMMENT '需求故事的状态',
  `srms` varchar(32) DEFAULT NULL COMMENT '需求号码',
  `srms_status` varchar(32) DEFAULT NULL COMMENT '需求状态',
  `team` varchar(32) DEFAULT NULL COMMENT '需求所属战队',
  `planned_bp` varchar(32) DEFAULT NULL COMMENT '平台版本',
  `verify_cost` bigint(20) DEFAULT NULL COMMENT '开发提测SQE周期 当前版本VDR所关联SRMS从solution到Verify的所用时间，单位小时',
  `complete_cost` bigint(20) DEFAULT NULL COMMENT '提测DIO周期 当前版本VDR所关联SRMS从Verify到Complete的所用时间，单位小时',
  `ctask` varchar(32) DEFAULT NULL COMMENT '测试用例号码',
  `ctask_status` varchar(32) DEFAULT NULL COMMENT '测试用例状态',
  `qtask` varchar(32) DEFAULT NULL COMMENT '测试号码',
  `qtask_status` varchar(32) DEFAULT NULL COMMENT '测试状态',
  `create_datetime` datetime DEFAULT now() COMMENT '创建日期',
  `update_datetime` datetime DEFAULT now() COMMENT '更新日期',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1;
ALTER TABLE `dws_develop_requirement_cost_time_info_1d_a` ADD UNIQUE INDEX `uniq_vdr_srms` (`vdr`, `srms`) USING BTREE;
SET FOREIGN_KEY_CHECKS = 1;

DROP TABLE IF EXISTS `ads_develop_requirement_cost_time_info_1d_i`;
CREATE TABLE `ads_develop_requirement_cost_time_info_1d_i` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `planned_bp` varchar(32) DEFAULT NULL COMMENT '平台版本',
  `team` varchar(32) DEFAULT NULL COMMENT '需求所属战队',
  `vdr` bigint(20) DEFAULT NULL COMMENT '当前版本不在Discard状态的VDR Story数',
  `vdr_handshake` bigint(20) DEFAULT NULL COMMENT '当前版本不在Open或Discard状态的VDR Story数',
  `vdr_disassemble` bigint(20) DEFAULT NULL COMMENT '当前版本关联SRMS且SRMS到Solution，Verify，Feature Missing，Complete状态的VDR Story数',
  `vdr_verify` bigint(20) DEFAULT NULL COMMENT '当前版本关联SRMS且SRMS到Verify状态的VDR Story数',
  `vdr_complete` bigint(20) DEFAULT NULL COMMENT '当前版本关联SRMS且SRMS到Verify状态的VDR Story数',
  `vdr_implement` bigint(20) DEFAULT NULL COMMENT '当前版本关联SRMS且SRMS到Verify，Complete状态的VDR Story数',
  `ctask_done` bigint(20) DEFAULT NULL COMMENT '测试用例已完成的VDR Story数',
  `qtask_done` bigint(20) DEFAULT NULL COMMENT '测试已完成的VDR Story数',
  `handshake_rate` double DEFAULT NULL COMMENT '需求握手率',
  `disassemble_rate` double DEFAULT NULL COMMENT '需求拆解率',
  `implement_rate` double DEFAULT NULL COMMENT '需求实现率',
  `ctask_done_rate` double DEFAULT NULL COMMENT '针对需求的测试用例覆盖率',
  `qtask_done_rate` double DEFAULT NULL COMMENT '针对需求的测试覆盖率',
  `verify_cost` double DEFAULT NULL COMMENT '开发提测SQE周期 当前版本VDR所关联SRMS从solution到Verify的所用时间，单位小时',
  `complete_cost` double DEFAULT NULL COMMENT '提测DIO周期 当前版本VDR所关联SRMS从Verify到Complete的所用时间，单位小时',
  `event_time` varchar(64) DEFAULT NULL COMMENT '事件日期',
  `create_datetime` datetime DEFAULT now() COMMENT '创建日期',
  `update_datetime` datetime DEFAULT now() COMMENT '更新日期',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;
ALTER TABLE `ads_develop_requirement_cost_time_info_1d_i` ADD UNIQUE INDEX `uniq_vdr_srms` (`planned_bp`, `team`, `event_time`) USING BTREE;
SET FOREIGN_KEY_CHECKS = 1;
