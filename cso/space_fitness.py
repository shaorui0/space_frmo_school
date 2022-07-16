import numpy as np
import random
    
# i 类导弹 打击 第 j 个目标
def Attack_revenue(N, value, p_rate):
    ans, t = 0, len(p_rate[0])
    for j in range(t):
        ans += value[j] * ptotal(p_rate,N,j)
    
    x = N[0]
    y = N[1]
    ans = ans + 2*x*y + 2*x - x**2 - 2*(y**2)
    return ans

def ptotal(p_rate, N, j: int):
    total, m = 1.0, len(p_rate)
    for i in range(m):
        # print("ptotal", p_rate, i, j)
        # print("n", N, i, j)
        # total *=  (1 - p_rate[i][j]) ** N[i][j]
        total *=  (1 - p_rate[i][j]) ** N[i]
    return 1 - total

# demention = 2
# p_rate = [[0.5,0.5],[0.5,0.5]]
# n = [[1,1],[1,1]]
# value = [1,1]
# # 参数： p_rate：矩阵，n：矩阵，value：数组, m行t列
# # # print(ptotal(p_rate,N,0))
# # print(Attack_revenue(p_rate=p_rate,n=N,value=value))
# TODO 看论文进行解释，每个参数怎么获取

# p 是打击率 --- 固定的
# n 是 xij 最终分配方案 --- 变化的
# value 是每个目标的价值 --- 固定的

def fitness_space(X):
    X = np.array(X).reshape(-1,1)
    p_rate = get_p_rate_from_db(len(X), len(X[0]))
    value = get_enemy_value_from_db(len(X[0]))
    
    # X = np.array(X).reshape(-1,1)
    X_array = list()
    for i in range(len(X)):
        X_array.append(X[i][0])
    
    return Attack_revenue(X_array, value, p_rate)

def get_p_rate_from_db(combat_num, enemy_num):
    '''几类导弹 打击 几类目标
    '''
    # print("TODO get_p_rate_from_db")
    # random generate
    res = []
    random.seed(42)
    for _ in range(combat_num):
        temp = []
        for _ in range(enemy_num):
            temp.append(random.random())
        res.append(temp)
        
    return res

def get_enemy_value_from_db(enemy_num):
    """目标价值
    """
    # print("TODO get_enemy_value_from_db")
    temp = []
    for _ in range(enemy_num):
        temp.append(random.random())
    return temp
