DROP TABLE IF EXISTS `mysql_schema_info`;
CREATE TABLE `mysql_schema_info` (
  `id` int(11) NOT NULL  AUTO_INCREMENT COMMENT 'ID',
  `cluster_name` varchar(50)  NOT NULL DEFAULT ''  COMMENT '集群名称',
  `dbhost` varchar(40) NOT NULL DEFAULT '' COMMENT '主机地址',
  `dbport` int(11) NOT NULL DEFAULT 3306 COMMENT '端口',
  `dbrule` varchar(50)  NOT NULL DEFAULT ''  COMMENT '角色',
  `dbservice` varchar(50)  NOT NULL DEFAULT ''  COMMENT '所属业务线',
  `dbuser` varchar(50) NOT NULL DEFAULT '' COMMENT '用户名',
  `dbpasswd` varchar(300) NOT NULL DEFAULT '' COMMENT '密码',
  `dbdevelopment` varchar(50) NOT NULL DEFAULT '' COMMENT '开发',
  PRIMARY KEY (`id`),
  UNIQUE KEY uniq_host_port (dbhost,dbport)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

insert into mysql_schema_info values (1,'xrj','172.168.1.10',5717,'master','新融街','che','che123','谷建梃');
insert into mysql_schema_info values (2,'xrj','172.168.1.11',5717,'slave','新融街','che','che123','谷建梃');
insert into mysql_schema_info values (3,'xrj','172.168.1.12',5717,'slave','新融街','che','che123','谷建梃');
insert into mysql_schema_info values (4,'jijin','172.168.1.12',5700,'master','基金','che','che123','郭星');
insert into mysql_schema_info values (5,'jijin','172.168.1.10',5700,'slave','基金','che','che123','郭星');