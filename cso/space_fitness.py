import numpy as np
import random
import data_generator
random.seed(42)


def fitness_space(X):
    '''cso fitness function
    '''
    X = np.array(X).reshape(-1,1)
    p_rate = data_generator.get_p_rate_from_db(len(X), len(X[0]))
    value = data_generator.get_enemy_value_from_db(len(X[0]))
    
    X_array = list()
    for i in range(len(X)):
        X_array.append(X[i][0])
    
    return attack_revenue(X_array, value, p_rate)

# i 类导弹 打击 第 j 个目标
def attack_revenue(N, value, p_rate):
    """参数： p_rate：矩阵，n：矩阵，value：数组, m行t列
    n 是 xij 最终分配方案 --- 变化的
    value 是每个目标的价值 --- 固定的
    p_rate 是打击率 --- 固定的
    """
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
        total *=  (1 - p_rate[i][j]) ** N[i]
    return 1 - total
