import random
from sys import argv
from log import log
def get_p_rate_from_db(combat_num, enemy_num):
    '''几类导弹 打击 几类目标
    '''
    res = []
    for _ in range(combat_num):
        temp = []
        for _ in range(enemy_num):
            temp.append(random.random())
        res.append(temp)
        
    return res

def get_enemy_value_from_db(enemy_num):
    """目标价值
    """
    temp = []
    for _ in range(enemy_num):
        temp.append(random.random())
    return temp

def get_combat_data_from_db(combat_id):
    log.info("get_combat_data_from_db: {}".format(combat_id))
    return {
        "combat_id": combat_id, # 导弹车号
        "name": combat_id,
        "resource_type": combat_id,  # 1类导弹车                      
        "coordinate": _genenrate_coordinate(), # 当前坐标，规定范围 1000,1000?
        "value": 0.1,
    }

def get_enemy_data_from_db(enemy_id):
    return {
        "enemy_id": enemy_id, # 导弹车号
        "name": enemy_id,
        "resource_type": enemy_id,  # 1类导弹车                      
        "coordinate": _genenrate_coordinate(), # 当前坐标，规定范围 1000,1000?
        "value": 0.1,
    }

def get_downside_data(level, zhuyu, weiyu, bingyu):
    log.info("get_downside_data before: {} {} {} {}".format(level, zhuyu, weiyu, bingyu))
    if level == 2:
        zhuyu = ["c_7_4_1", "c_7_4_2", "c_7_4_3", "c_7_4_4", "c_7_4_5"] # 有4个导弹车，id 为1/2/3/4
        weiyu = "hit"
        bingyu = ["m_749_1", "m_749_2", "m_749_3"] # 敌人 - 有3个体单位，id 为1/2/3
    elif level == 1:
        zhuyu = ["c_7_4"] # 营级别
        weiyu = "hit"
        bingyu = ["m_749"] # 敌人 - 营级别
    else:
        raise Exception("not exist the level.")
    log.info("get_downside_data end: {} {} {} {}".format(level, zhuyu, weiyu, bingyu))
    return zhuyu, weiyu, bingyu

def _genenrate_coordinate():
    '''获取坐标
    '''
    x = random.randint(0,1000) 
    y = random.randint(0,1000)
    return str(x) + "_" + str(y)