CREATE database space;
use space;
--- 表创建
CREATE TABLE IF NOT EXISTS `military_resource`(
    `id` INT UNSIGNED AUTO_INCREMENT,
   `military_resource_id` VARCHAR(40) NOT NULL COMMENT '旅:ax, 如a1 / 营:bx, 如b1',
   `name` VARCHAR(40),
   `resource_type` INT(10) NOT NULL COMMENT '旅:1，营:2',
   `superior` VARCHAR(10) NOT NULL COMMENT '上级id，旅上级为"0"，营上级为旅id',
   `coordinate` VARCHAR(20) NOT NULL COMMENT '当前坐标',
   `shape` VARCHAR(200) COMMENT 'item图标url',
   `status` INT(10) DEFAULT 1 COMMENT '生:1/死:0',
   `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
   `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY ( `id` ),
    unique key  ( `military_resource_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `combat_resource`(
    `id` INT UNSIGNED AUTO_INCREMENT,
   `combat_resource_id` VARCHAR(40) NOT NULL ,
   `name` VARCHAR(40) NOT NULL,
   `resource_type` INT(10) NOT NULL COMMENT '资源类型，导弹:1, 通讯:2, 传感器:3',
   `belong_to` VARCHAR(40) NOT NULL COMMENT '属于哪个军队资源', 
   `coordinate` VARCHAR(20) NOT NULL COMMENT '当前坐标',
   `shape` VARCHAR(200) NOT NULL COMMENT 'item图标url',
   `status` INT(10) NOT NULL DEFAULT 1 COMMENT '生:1/死:0',
   `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
   `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
   PRIMARY KEY ( `id` ),
   unique key  ( `combat_resource_id` ),
   FOREIGN KEY(belong_to) REFERENCES military_resource(military_resource_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `enemy_resource`(
    `id` INT UNSIGNED AUTO_INCREMENT,
   `enemy_resource_id` VARCHAR(40) NOT NULL,
   `name` VARCHAR(20) NOT NULL,
   `shape_type` INT(10) NOT NULL COMMENT '运行轨迹类型',
   `coordinate` VARCHAR(20) NOT NULL COMMENT '当前坐标',
   `status` INT(1) NOT NULL DEFAULT 1 COMMENT '生:1/死:0',
      `shape` VARCHAR(200) NOT NULL COMMENT 'item图标url',
   `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
   `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
      unique key  ( `enemy_resource_id` ),
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;



--- 数据创建

--- 军队资源

INSERT INTO military_resource  (military_resource_id, name,resource_type, superior , coordinate, shape)  VALUES  ('a1', 'name', 1, '0', '200_200', 'url');
INSERT INTO military_resource  (military_resource_id, name,resource_type, superior, coordinate, shape)  VALUES  ('a2', 'name', 1, '0', '200_300', 'url');

INSERT INTO military_resource  (military_resource_id, name,resource_type, superior,  coordinate, shape)  VALUES  ('b1', 'name', 2, 'a1',  '200_500', 'url');
INSERT INTO military_resource  (military_resource_id, name,resource_type, superior,  coordinate, shape)  VALUES  ('b2', 'name', 2, 'a1',  '200_500', 'url');

INSERT INTO military_resource  (military_resource_id, name,resource_type, superior,  coordinate, shape)  VALUES  ('b3', 'name', 2, 'a2',  '200_500', 'url');
INSERT INTO military_resource  (military_resource_id, name,resource_type, superior,  coordinate, shape)  VALUES  ('b4', 'name', 2, 'a2',  '200_500', 'url');
INSERT INTO military_resource  (military_resource_id, name,resource_type, superior,  coordinate, shape)  VALUES  ('b5', 'name', 2, 'a2',  '200_500', 'url');

--- 【注】每次插两条记录，上级和下级都需定义一便

--- 作战资源

INSERT INTO combat_resource  (combat_resource_id, name,resource_type, belong_to,  coordinate, shape)  VALUES  ('m1', 'name', 1,  'b1', '210_500', 'url');
INSERT INTO combat_resource  (combat_resource_id, name,resource_type, belong_to,  coordinate, shape)  VALUES  ('m2', 'name', 1,  'b2', '220_500', 'url');
INSERT INTO combat_resource  (combat_resource_id, name,resource_type, belong_to,  coordinate, shape)  VALUES  ('c1', 'name', 2,  'b3', '230_500', 'url');
INSERT INTO combat_resource  (combat_resource_id, name,resource_type, belong_to,  coordinate, shape)  VALUES  ('c2', 'name', 2,  'b4', '240_500', 'url');
INSERT INTO combat_resource  (combat_resource_id, name,resource_type, belong_to,  coordinate, shape)  VALUES  ('s1', 'name', 3,  'b5', '250_500', 'url');
INSERT INTO combat_resource  (combat_resource_id, name,resource_type, belong_to,  coordinate, shape)  VALUES  ('s2', 'name', 3,  'b5', '260_500', 'url');


--- 敌方资源

INSERT INTO enemy_resource  (enemy_resource_id, name,shape_type,   coordinate, shape)  VALUES  ('r1', 'name', 1,  '260_500', 'url');
INSERT INTO enemy_resource  (enemy_resource_id, name,shape_type,   coordinate, shape)  VALUES  ('r2', 'name', 2,  '260_500', 'url');
INSERT INTO enemy_resource  (enemy_resource_id, name,shape_type,   coordinate, shape)  VALUES  ('r3', 'name', 3,  '260_500', 'url');


-- drop table combat_resource;
-- drop table military_resource;
-- drop table enemy_resource;

--- 检查插入
select * from military_resource;
select * from combat_resource;
select * from enemy_resource;
--- 数据获取
--- 找到敌方资源的运行轨道类型（圆、正方形...）
select shape_type from enemy_resource where enemy_resource_id = 'r3';

--- 获取b3营上级
select superior from military_resource where military_resource_id = 'b3';
--- 获取a1旅下级 
select military_resource_id from military_resource where superior = 'a1';

--- 获取b2营（军队资源）的导弹车id
SELECT combat_resource_id FROM combat_resource 
INNER JOIN military_resource ON combat_resource.belong_to = military_resource.military_resource_id
WHERE military_resource.military_resource_id = 'b2' and combat_resource.resource_type = 1;


--- 数据更新

--- 更新状态（死/0、活/1）

update status=0 from yyy where  enemy_resource_id = '1';
update status=1 from yyy where  enemy_resource_id = '1';

--- 更新坐标

update coordinate='1_1' from military_resource where  military_resource_id = '1';
update coordinate='2_1' from combat_resource where  combat_resource_id = '1';
update coordinate='3_1' from enemy_resource where  enemy_resource_id = '1';

