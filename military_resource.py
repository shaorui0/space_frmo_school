import time
import os
import json

import random
from log import with_log, log

g_military_resource = dict()
g_combat_resource = dict()

# # TODO 模拟军事资源
# army1 = ArmyV1("a1", 1, "commander_name", "0", ["b1", "b2"], "222_111", ["m1", "c1", "s1"])
# g_military_resource["a1"] = army1
# # ...

# # TODO 模拟作战资源


# # ...
@with_log   
class MilitaryResource(object): 
    BRIGADE_TYPE = 1  # 旅

    def __init__(self, 
            military_resource_id,
            resource_type,                                              #军队资源级别
            commander_name,                              #军队长官姓名
            superior,                                        #直属上级id
            subordinates,                                   #直属下级id
            coordinate,                                       # 当前坐标
            combat_source_ids,       
            ):
        self.military_resource_id=military_resource_id                                                #军队资源id
        self.resource_type=resource_type                                              #军队资源级别
        self.commander_name =commander_name                             #军队长官姓名
        self.superior =superior                                        #直属上级id
        self.subordinates=subordinates                                 #直属下级id
        self.coordinate=coordinate                                 # 当前坐标
        self.status = True                                  # 当前状态
        self.combat_source_ids=combat_source_ids     #该资源单位的作战资源

    def run_command_from_terminal(self,command_str): # 张立波界面调用
        """ 从界面读取命令并执行
        input: command_str
        output: print_str, 用于前端界面显示当前系统执行情况
        """
        # 解析字符串，未来的解析更复杂
        subj, predic, obj = self.parse_command(command_str)
        
        # 判断当前是旅还是营，如果是旅，随机找到一个下属营
        if g_military_resource[subj].resource_type == self.BRIGADE_TYPE: # 旅
            new_subj = self.random_find_a_subordinate() # TODO 随机找到一个下属营（转为营的状态执行下面任务）
            # TODO log
            subj = new_subj

        self.log.debug("当前命令：{}".format(predic))
        

        # 营：
        if predic == "hit": # "攻击":
            try:
                new_hiter_id = self.random_find_a_missile_vehicle() 
                g_combat_resource[new_hiter_id].attack(obj) # 调用王强的攻击函数
                self.log.debug("command: '{}' 执行成功".format(command_str))
            except Exception as e:
                # 返回给终端对话框相关信息
                self.log.error(e)
                return str(e)
        elif predic == "move": # 移动
            if subj[0] in set(a, b): # military_resource （a/b开头）
                g_military_resource[subj].move(obj) # 陈岩实现的移动函数
            elif subj[0] in set(a, b): # combat_resource（m/c/r开头）
                g_combat_resource[subj].move(obj)  # 王强实现的移动函数
            self.log.debug("command: '{}' 执行成功".format(command_str))
        else:
            return "当前未实现相关命令"

    def random_find_a_missile_vehicle(self): # 随机找到一辆 导弹车 id
        for id in self.combat_source_ids.keys():
            if id[0] == 'm': # m 为导弹车前缀
                return id
        raise Exception("当前营下没有导弹车")
    
    def random_find_a_subordinate(self):
        # TODO 实现数组里随机返回idx
        # DONE
        return random.sample(self.subordinates,1)
        

    def move(self, new_coordinate):
        """移动
        """
        self.coordinate = new_coordinate
        # update global map 
        g_military_resource[self.military_resource_id] = self #不需要更新吧
        # TODO update database
        sql = "update coordinate='{}' from military_resource where  military_resource_id = '{}';".format(new_coordinate, self.military_resource_id)

        # TODO update main window。调用“刷新功能”对窗口进行刷新

        return

    def parse_command(self, command_str):
        # TODO 主, 谓, 宾。 未来可能是更复杂的字符串处理
        # 标准化命令格式：
            # 攻击："a1 hit r3"
            # 移动："a1 move 222_333" / "m1 move 100_200"
        return command_str.split(' ')
    
    # def sendCommand(self,id,command='hello'):
    #     # 主要用于多机命令传输，目前不需要
    #     pass

    # def receiveCommand(self,):
    #     # 主要用于多机命令传输，目前不需要                         
    #     pass
    

    # def getSource(self,):
    #     return self.combatSource.getSource
    #     pass
    # def getSuperior(self,):
    #     # return object
    #     pass
    # def getSubordinates(self,):
    #     # return list(object)
    #     pass
    # def logInsert(self,):
    #     pass


# '''
# 具体功能需要讨论

# state:doing
# '''

# class Army: 
#     military_resource_id=0                                                #军队资源id
#     resource_type=0                                              #军队资源级别
#     commander_name ='hello'                             #军队长官姓名
#     superior =12                                        #直属上级id
#     subordinates=[]                                    #直属下级id
#     coordinate=[]                                       # 当前坐标
#     status = threadQueue                                  # 当前状态
#     combatSource_ids=[]                                  #该资源单位的作战资源

#     idMapIP={'123':('127.0.0.1',1236)}                  #需要一个用来存储个个单位通信ip和port的dict 此映射表用于 命令和数据收发时 通信
#     def __init__(self,commuPort=1234):
#         self.commu=Communication(port=commuPort)
#     def sendCommand(self,id,command='hello'): #命令暂时定为str'
#         addr=self.idMapIP['123']
#         self.commu.sendBuffer(addr[0],addr[1],command)        
#         pass
#     def receiveCommand(self,):                          #从命令缓存中读取一条指令 {‘addr':addr,'data':command}
#         self.commu.lock.acquire()
#         data=self.commu.commandQueue.pop(0)     
#         self.commu.lock.release()
#         return data    
#         pass
#     def getSource(self,):
#         return self.combatSource.getSource
#         pass
#     def getSuperior(self,):
#         # return object
#         pass
#     def getSubordinates(self,):
#         # return list(object)
#         pass
#     def logInsert(self,):
#         pass
