# from combat_resource import Attacker
import combat_resource
import enemy_resource
from log import with_log, log
from cso import cso, space_fitness, run
import random
import data_generator

random.Random(43)
    
@with_log  
class InputProcess():
    def __init__(self, input_str):
        self.input_str = input_str
    
    def main_process(self):
        # TODO 胡琛处理输入，进行分解主谓宾
        self.log.info("胡琛处理输入，进行分解主谓宾")
        zhuyu = "七团四营"
        weiyu = "攻击"
        bingyu = "749高地"

        # 对字符串进行进一步解析成字符 --- 有一个全局 mapping 就可以了
        self.log.info("对字符串进行进一步解析成字符")
        LEVEL_1 = 1
        zhuyu_1, weiyu_1, bingyu_1 = data_generator.get_downside_data(LEVEL_1, zhuyu, weiyu, bingyu)
        
        self.log.info("对每一个主谓宾进行解析")
        ### 本质上是从 DB 中获取1营下有几个导弹车 --- 目前设定一个导弹车只有一枚导弹，可能是不同类型，未来可能增加更多层次（即一辆导弹车有多枚导弹）
        LEVEL_2 = 2
        zhuyu_2, weiyu_2, bingyu_2 = data_generator.get_downside_data(LEVEL_2, zhuyu_1, weiyu_1, bingyu_1)

        self.log.info("正在获取 item 坐标 + item 基本数据......")
        combat_obj_map, combat_coordination_map = self._get_total_combat_resource(zhuyu_2)
        log.info("combat_obj_map: {}".format(combat_coordination_map))
        enemy_obj_map, enemy_coordination_map = self._get_total_enemy_resource(bingyu_2)
        log.info("enemy_obj_map".format(enemy_obj_map, enemy_coordination_map))
        
        self.log.info("正在解析出哪些导弹打哪些车......")
        final_hit_map = self.handle_mapping_relationship(combat_obj_map, enemy_obj_map)

        self.log.info("根据 map 生成最终命令......")
        output_text = self._parse_final_map(final_hit_map)
        return output_text, combat_coordination_map, enemy_coordination_map, final_hit_map
        
    def handle_mapping_relationship(self, combat_obj_map, enemy_obj_map):
        """分析业务逻辑，combat 如何选择 enemy 打击目标
        """
        log.info("具体逻辑：几类导弹有几颗，打击几个敌方 {} {}".format(combat_obj_map, enemy_obj_map))
        # 数据预处理，把idx 和 id/name/type 对应起来
        combat_num_map = dict() # 每种类型的导弹有几颗
        combat_type_ids_map = dict() # 每种类型的导弹都是哪些导弹车id
        for k, v in combat_obj_map.items():
            log.info("combat_obj_map: {} {}".format(k, v))
            if v.id not in combat_num_map:
                combat_num_map[v.resource_type] = 0
            combat_num_map[v.resource_type] += 1
            
            if v.resource_type not in combat_type_ids_map:
                combat_type_ids_map[v.resource_type] = list()
            combat_type_ids_map[v.resource_type].append(v.id) 
            
        enemy_type_ids_map = dict() # 每种类型的敌人都是什么id
        for k, v in enemy_obj_map.items():
            log.info("enemy_obj_map: {} {}".format(k, v))
            if v.resource_type not in enemy_type_ids_map:
                enemy_type_ids_map[v.resource_type] = list()
            enemy_type_ids_map[v.resource_type].append(v.id)

        log.info("combat_type_ids_map {}".format(combat_type_ids_map))
        log.info("enemy_type_ids_map {}".format(enemy_type_ids_map))
        
        self.log.info(">>> 正在进行布谷鸟搜索......")
        final_rounded_mapping_res = run.runCSO(combat_obj_map, enemy_obj_map)
        log.info("final_rounded_mapping_res: {}".format(final_rounded_mapping_res))
        
        # TODO list to mapping? 
        # 几号打几号 (类和号相等，for now)
        # final_map = {idx: final_rounded_mapping_res[idx] for idx in range(len(final_rounded_mapping_res))}
        # log.info("final_map result: ", final_map)
        
        return final_rounded_mapping_res
    
    def _parse_final_map(self, final_map):
        # TODO 解析
        final_str = ""
        for k, v in final_map.items():
            final_str += "我方 {} 打击 敌方 {}\n".format(k, v)
        return final_str
    
    def _get_total_combat_resource(self, zhuyu_2):
        self.log.info("处理所有的战斗资源")
        combat_coordination_map = {
                "name": [],
                "x": [],
                "y": [],
            }
        combat_obj_map = dict()
        for combat_id in zhuyu_2:
            log.info("combat_id: {}".format(combat_id))
            combat_data = data_generator.get_combat_data_from_db(combat_id)
            combat_obj_map[combat_id] = combat_resource.CombatResource(
                id=combat_data['combat_id'], # 导弹车号
                name=combat_data['name'],
                resource_type=combat_data['resource_type'],  # 1类导弹车                      
                coordinate=combat_data['coordinate'], # 当前坐标，规定范围 1000,1000?
                value = combat_data['value'],
            )
            
            combat_coordination_map["name"].append(combat_data['name'])
            x, y = combat_data['coordinate'].split("_")
            combat_coordination_map["x"].append(x)
            combat_coordination_map["y"].append(y)
        
        return combat_obj_map, combat_coordination_map
    
    def _get_total_enemy_resource(self, bingyu_2):
        self.log.info("处理所有的敌方单位")
        enemy_obj_map = dict()
        enemy_coordination_map = {
                "name": [],
                "x": [],
                "y": [],
            }
        
        for enemy_id in bingyu_2:
            enemy_data = data_generator.get_enemy_data_from_db(enemy_id)
            enemy_obj_map[enemy_id] = enemy_resource.EnemyResource(
                id=enemy_data['enemy_id'], # 导弹车号
                name=enemy_data['name'],
                resource_type=enemy_data['resource_type'],  # 1类导弹车                      
                coordinate=enemy_data['coordinate'], # 当前坐标，规定范围 1000,1000?
                value = enemy_data['value'],
            )
            
            enemy_coordination_map["name"].append(enemy_data['name'])
            x, y = enemy_data['coordinate'].split("_")
            enemy_coordination_map["x"].append(x)
            enemy_coordination_map["y"].append(y)
        
        return enemy_obj_map, enemy_coordination_map

