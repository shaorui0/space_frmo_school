from cso import CSO
import fitness

print("正在进行布谷鸟搜索......")
CSO(fitness=fitness.fitness_4, bound=[(-4,4),(-4,4)], min=False).execute()