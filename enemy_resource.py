import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtWidgets import QGraphicsItem, QWidget
import math

#敌方单位
class EnemyResource(object):
    def __init__(self, 
            enemy_resource_id,
            resource_type,                                              #军队资源级别
            coordinate,                                       # 当前坐标
            value,  # 敌人价值
            ):
        self.enemy_resource_id=enemy_resource_id                                                #军队资源id
        self.resource_type=resource_type                                              #军队资源级别
        self.coordinate=coordinate                                 # 当前坐标
        self.value=value


class enemy_resource(QGraphicsItem):

    def __init__(self,  timer):
        super(enemy_resource, self).__init__()
        self.type = '1' #类型

        self.nowt = 0 #轨迹方程点
        self.T = 300 #周期
        self.direction = 1 #移动方向
        self.step = 1 #步长
        self.i = 0 #圆轨迹步长
        timer.timeout.connect(lambda: self.advance())

    def setBasePos(self,x,y):
        self.setPos(x, y)
        self.basePos = QPointF(x, y)

    def boundingRect(self) -> QtCore.QRectF:
        adjust = 0.5
        w = 15
        h = 20
        return QRectF(-w-adjust, -h-adjust, w+adjust, h+adjust)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem', widget: typing.Optional[QWidget] = ...):
        painter.setBrush(Qt.green)
        painter.drawRect(self.boundingRect())
        painter.setBrush(Qt.black)
        painter.drawText(self.boundingRect(), self.type)

    #移动
    def advance(self):
        x,y=self.line(80.1)
        self.setPos(x,y)

    #直线轨迹
    def line(self,rate):
        oldt = self.nowt
        self.nowt += self.direction * self.step
        if (self.nowt <= 0):
            self.direction = 1
        elif (self.nowt >= self.T):
            self.direction = -1
        oldx, oldy = oldt * math.cos(rate), oldt * math.sin(rate)
        x = self.nowt * math.cos(rate) - oldx + self.pos().x()
        y = self.nowt * math.sin(rate) - oldy + self.pos().y()
        return x, y

class enemy_resource_1(enemy_resource):

    def __init__(self, timer):
        super(enemy_resource_1, self).__init__(timer)

    def advance(self):
        x,y=self.circle(50)
        self.setPos(x,y)

    #圆形轨迹
    def circle(self,lens):
        oldar =( int(self.i)  % (int(3.1415*10000*2) * 1000) ) / 10000000
        self.i += int(3.1415*10000) * 5
        self.i = int(self.i)  % (int(3.1415*10000*2) * 1000)
        ar = self.i / 10000000
        x = lens * math.cos(ar)  - lens * math.cos(oldar) + self.pos().x()
        y = lens * math.sin(ar)  - lens * math.sin(oldar) + self.pos().y()
        return x, y















