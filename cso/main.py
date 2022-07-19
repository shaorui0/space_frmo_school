from cso import CSO
import fitness, space_fitness
from log import log

log.info("正在进行布谷鸟搜索......")
# CSO(fitness=fitness.fitness_4, bound=[(-4,4),(-4,4)], min=False).execute()
res = CSO(fitness=space_fitness.fitness_space, bound=[(0,3),(0,3),(0,3),(0,3),(0,3)], n=5, min=False).execute()


def mapping(a_float_list):
    return [round(x) for x in a_float_list]

log.info(mapping(res))