"""
用于持久化：
1. 加载 load_all_data
2. 保存
3. 刷新
"""

g_military_resource = dict()
g_combat_resource = dict()
g_enemy_resource = dict()

def load_all_data():
    military_resource_load_sql = "select military_resource_id, resource_type, superior, coordinate, status from military_resource;"
    combat_resource_load_sql = "select combat_resource_id, resource_type, belong_to, coordinate, status from military_resource;"
    enemy_resource_load_sql = "select enemy_resource_id, shape_type, coordinate, status from military_resource;"
    try:
        military_resource_result = mysql_connector.run_sql(military_resource_load_sql)
        combat_resource_result = mysql_connector.run_sql(combat_resource_load_sql)
        enemy_resource_result = mysql_connector.run_sql(enemy_resource_load_sql)
    except:
        raise Exception("执行sql发生异常")


    # 批量创建
    # 1. 军事资源
    for military_resource in military_resource_result:
        # TODO mysql执行出来是什么形式？
        military_resource_id = military_resource.military_resource_id
        # ...
        
        army = ArmyV1(military_resource_id, 1, "commander_name", "0", ["b1", "b2"], "222_111", ["m1", "c1", "s1"])
        g_military_resource[military_resource_id] = army # loading
        # 
    
    log.debug(g_military_resource) # TODO test

    # 2. 作战资源
    # 

    # 3. 敌方资源

def store_all_data():
    """
    将所有全局单位持久化到数据库
    """
    TODO