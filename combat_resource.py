import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QGraphicsEllipseItem
import math

from enemy_resource import enemy_resource

class CombatResource(object):
    def __init__(self, id, carType, coordinate, value):
        super(car, self).__init__()
        self.id = id  # 车辆唯一标识id
        self.carType = carType  # 车辆类型,限定四种类型 1.Attacker 2.observer 3.communicator 4.commander
        self.coordinate = coordinate # (0,0)  # 地图坐标,格式x_y
        self.value = value

class car(QGraphicsItem):

    def __init__(self, id, carType, coordinate, value):
        super(car, self).__init__()
        self.id = id  # 车辆唯一标识id
        self.carType = carType  # 车辆类型,限定四种类型 1.Attacker 2.observer 3.communicator 4.commander
        # self.name = name  # 车辆名称
        # self.belong_id = belong_id  # 归属于哪一级military_resource
        self.coordinate = coordinate # (0,0)  # 地图坐标,格式x_y
        self.value=value

class Attacker(car):
    
    def __init__(self, id, carType, name, belong_id,timer):
        super(Attacker, self).__init__(id,carType,name,belong_id)
        self.aimPos = QPointF(-1, -1)
        self.speed = 3
        self.timer = timer
        self.timer.timeout.connect(lambda: self.advance())
        self._brush = QBrush(Qt.yellow)
        self.statues = 0

    def setBasePos(self,x,y):
        self.setPos(x, y)

    #设置单位形状
    def boundingRect(self) -> QtCore.QRectF:
        adjust = 0.5
        w = 20
        h = 30
        # return QRectF(-w - adjust, -h - adjust, w + adjust, h + adjust)
        return QRectF(-200 - adjust, -200 - adjust, 200 + adjust, 200 + adjust)

    #绘制单位
    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem',widget: typing.Optional[QWidget] = ...):
        if self.statues == 1:
            self.setBrush(QBrush(Qt.red))
            painter.setBrush(QBrush(Qt.white))
            painter.drawEllipse(QRectF(-100,-100,100,100))
        painter.setBrush(self._brush)
        painter.drawRect(QRectF(-20.5,-30.5,20.5,30.5))
        painter.setBrush(Qt.black)
        painter.drawText(QRectF(-20.5,-30.5,20.5,30.5), self.carType)
        self.update()

    def setBrush(self, brush):
        self._brush = brush
        self.update()

    #移动
    def advance(self):
        if self.aimPos.x() <= 0:
            return
        p = self.aimPos - self.pos()
        l = math.sqrt(p.x()*p.x() + p.y()*p.y())
        if l < 0.00001:
            self.aimPos = QPointF(-1, -1)
            return
        dis = self.speed
        if dis > l:
            dis = l
        self.setPos(self.mapToParent(dis/l*p))

# 指挥车
class commander(car):

    def __init__(self, timer):
        self.childern_ids = []          # 数组存放管理的车辆id,数据类型list
        self.owned_resource = {}        # 该辆指挥车所拥有的各种资源,数据类型dict

    # 该指挥车名下车辆汇报位置
    def query_subordinates_location(self):  
        list = []
        for child in self.childern_ids: 
            list.append(child)    
        return list  

    def query_subordinates_resource(self,id):
        self.owned_resource['server_bandwidth'] += id.server_bandwidth
        self.owned_resource['server_delay'] += id.server_delay
        self.owned_resource['server_capacity'] += id.server_capacity
    
    def deliver_command(self):
        pass

# 通讯车
class communicator(car,QGraphicsItem):

    def __init__(self, timer):
        self.curLevel = 0               # 当前层级
    
    def show_level(self):
        pass
    # show_level
    #         - desc: 展示层级关系
    #         - output:
    #             - TreeNode<Car> root    //返回生成关系树的根节点 
    #             class TreeNode {
    #                 Car curCar;
    #                 TreeNode<Car>  childCars;
    #             }

    def can_connect(self,id):
        limit_dist = 10000                      # 限制距离
        list1 = self.coordinate.split('-')
        list2 = id.coordinate.split('-')
        dist = math.sqrt(pow(list1[0]-list2[0],2)+pow(list1[1]-list2[1],2))
        if(limit_dist>dist):
            return True
        else:
            return False

    def connect_combat_resource(self):
        pass
    # - connect_combat_resource
    #         - desc: 发送对应作战意图,对应多种数据输入
    #         - input:
    #             - 不同数据输入
    #         - output:
    #             - boolean is_success

# 导弹
class missile(QGraphicsItem):

    def __init__(self, timer):
        super(missile, self).__init__()

        self.aim = None
        self.speed = 3 #速度
        self.timer = timer #计时器
        self.timer.timeout.connect(lambda: self.advance())
        self.mainview = None
        self.target = None

    def setBasePos(self,x,y):
        self.setPos(x, y)

    #设置单位形状
    def boundingRect(self) -> QtCore.QRectF:
        adjust = 0.5
        w = 5
        h = 5
        return QRectF(-w - adjust, -h - adjust, w + adjust, h + adjust)

    #绘制单位
    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem',widget: typing.Optional[QWidget] = ...):
        painter.setBrush(Qt.black)
        painter.drawRect(self.boundingRect())
        painter.setBrush(Qt.black)
        painter.drawText(self.boundingRect(), '')

    #移动
    def advance(self):
        self.aimPos = self.aim.pos()
        if self.aimPos.x() <= 0:
            return
        p = self.aimPos - self.pos()
        l = math.sqrt(p.x()*p.x() + p.y()*p.y())
        if l < 1:
            self.aimPos = QPointF(-1, -1)
            # self.setVisible(False)
            # self.collidingItems()[0].setVisible(False)
            self.mainview.scene.removeItem(self)
            self.mainview.scene.removeItem(self.target)
            return
        dis = self.speed
        if dis > l:
            dis = l
        self.setPos(self.mapToParent(dis/l*p))
























