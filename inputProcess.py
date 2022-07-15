from combat_resource import Attacker
import combat_resource
import enemy_resource
from log import with_log, log

@with_log  
class InputProcess():
    def __init__(self, input_str):
        self.input_str = input_str
        print("for debugging:", self.input_str)
    
    def main_process(self):
        # TODO
        # 胡琛处理输入，进行分解主谓宾
        self.log.info("胡琛处理输入，进行分解主谓宾")

        zhuyu = "我方1营"
        weiyu = "攻击"
        bingyu = "敌方1营"

        # 对字符串进行进一步解析成字符
        self.log.info("对字符串进行进一步解析成字符")
        zhuyu_1 = ["a_1"] # 营级别
        weiyu_1 = "hit"
        bingyu_1 = ["m_1"] # 敌人 - 营级别

        self.log.info("对每一个主谓宾进行解析")
        # 对每一个主谓宾进行解析
        ## TODO 需要获取数据库，对应的下属有哪些？
        ### 本质上是从 DB 中获取1营下有几个导弹车 --- 目前设定一个导弹车只有一枚导弹，可能是不同类型，未来可能增加更多层次（即一辆导弹车有多枚导弹）
        zhuyu_2 = ["a_1_1", "a_1_2", "a_1_3", "a_1_4"] # 有4个导弹车，id 为1/2/3/4
        weiyu_2 = "hit"
        bingyu_2 = ["m_1_1", "m_1_2", "m_1_3"] # 敌人 - 有3个体单位，id 为1/2/3

        # TODO 每个导弹车上的导弹有一些数据
        self.log.info("每个导弹车上的导弹有一些数据，再去查导弹车表（战斗资源）")
        ## 获取每个导弹的数据（有哪些数据项）
        ## 通过这些数据形成obj，然后装入
        combat_obj_map = dict()
        self.log.info("处理所有的战斗资源")
        for combat_id in zhuyu_2:
            # get data from DB
            
            # handle data if they need
            
            # create obj
            combat_obj = combat_resource.CombatResource(
                combat_resource_id=combat_id, # 导弹车号
                resource_type=1,  # 1类导弹车                               #直属下级id
                coordinate="", # 当前坐标，规定范围 1000,1000?
                value = 0.1,
            )
            # push obj to dict
            combat_obj_map[combat_id] = combat_obj

        # TODO 每个敌人有一些数据
        self.log.info("处理所有的敌方单位")
        ## 获取每个敌人的数据
        enemy_obj_map = dict()
        for enemy_id in bingyu_2:
            # get data from DB
            
            # handle data if they need
            
            # create obj
            enemy_obj = enemy_resource.EnemyResource(
                enemy_resource_id=enemy_id, # 导弹车号
                resource_type=1,  # 1类导弹车                               #直属下级id
                coordinate="", # 当前坐标，规定范围 1000,1000?
                value = 0.1,
            )
            # push obj to dict
            enemy_obj_map[enemy_id] = enemy_obj

        # TODO 解析出哪些导弹打哪些车
        final_map = self.get_mapping_between_peers(combat_obj_map, enemy_obj_map)


        final_map = {
            "a_1_1":"m_1_1",
            "a_1_2":"m_1_2",
            "a_1_3":"m_1_3",
            "a_1_4":"m_1_1"
        }

        # 根据 map 生成最终命令
        output_text = self.parse_final_map(final_map)

        # TODO 渲染 mainView

        self.log.info("渲染 mainView")
        return output_text

    def parse_final_map(self, final_map):
        # TODO 解析
        for k, v in final_map.items():
            print(k, " hit ", v)

    def get_mapping_between_peers(self, combat_obj_map, enemy_obj_map):
        # TODO 具体怎么样得到对应关系？业务逻辑重点
        self.log.info(combat_obj_map, enemy_obj_map)
        # 由上面的信息了，怎么进行映射
        # 具体逻辑：
        # 1. 几类导弹有几颗，打击几个敌方
        
        combat_num_map = dict() # 每种类型的导弹有几颗
        combat_type_ids_map = dict() # 每种类型的导弹都是哪些导弹车
        for k, v in combat_obj_map.items():
            print(k, v)
            if k.id not in combat_num_map:
                combat_num_map[k.carType] = 0
            combat_num_map[k.carType] += 1
            
            if k.carType not in combat_type_ids_map:
                combat_type_ids_map[k.carType] = list()
            combat_type_ids_map[k.carType].append(k.id)
            
        #     - 数据我也有了，那个表，我让王强跟着生成一下 mysql insert
        #         - 敌我双方的两张表
        #             - 坐标
        #             - ...
        #     - 同时也要元数据
        #         - 什么类型的我方 - 打击 -什么类型的敌方
        #             - 我方被毁概率
        #             - 敌方被毁概率
        #             - 这个我来设计一下？又得花时间
        #         - 这样一查
        #     - 主要是什么？我得写一下处理过程，能从mysql 拿到数据，然后分析出
        # 2. 具体我需要参考几个表，那些表我可以参考那篇论文
        enemy_type_ids_map = dict() # 每种类型的敌人都是什么id
        for k, v in enemy_obj_map.items():
            print(k, v)
            if k.carType not in enemy_type_ids_map:
                enemy_type_ids_map[k.carType] = list()
            enemy_type_ids_map[k.carType].append(k.id)
        
        # TODO 概率 + 价值
        combat_hit_rate_table = get_combat_hit_rate()
        enemy_hit_rate_table = get_enemy_hit_rate()

        ### 上面是数据准备，然后是计算
        # 我要能通过迭代求出一个最大值，引入那个布谷鸟算法
        
        

    ################# 渲染 mainView ##################
    def add_items(self):
        combat_T = Attacker()
        combat_T.type = 'T'
        combat_T.setPos(self.mapToScene(111, 111))
        self.scene.addItem(combat_T)
        # 先画自然的，然后更换icon

    def add_lines(self):
        pass

    def add_items_type_1(self):
        pass
        
    def add_items_type_2(self):
        pass
        
    def add_items_type_3(self):
        pass



def get_combat_hit_rate():
    pass

def get_enemy_hit_rate():
    pass