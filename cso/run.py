import cso 
from log import log

def runCSO(combat_obj_map, enemy_obj_map):
    combat_names = list(combat_obj_map.keys())
    enemy_names = list(enemy_obj_map.keys())
    
    len_combat = len(combat_obj_map) # 几颗导弹
    len_enemy = len(enemy_obj_map)
    bound = [(0, len_enemy) for i in range(len_combat)] # TODO 需要根据数据生成 
    n = len_combat
    log.info("bound: {}, n: {}".format(bound, n))
    mapping_res = cso.cso.CSO(fitness=cso.space_fitness.fitness_space, bound=bound, n=n, min=False).execute()
    rounded_mapping_res = [round(x) for x in mapping_res]
    log.info("CSO result: {}".format(rounded_mapping_res))
    
    final_map = {}
    for k, v in enumerate(rounded_mapping_res):
        if v == 0:
            v = 1 # TODO 
        final_map[combat_names[k]] = enemy_names[v-1]
    return final_map
    