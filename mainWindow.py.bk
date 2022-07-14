import math

import timer
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QObject, QTimer, QPointF, QMetaObject, QRect
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QWidget, QGraphicsView, QPushButton, QLineEdit, \
    QGraphicsEllipseItem

from combat_resource import Attacker, missile
from enemy_resource import enemy_resource, enemy_resource_1

class MainWindow(QMainWindow):

    sw = 1600; sh = 1200
    mainViewCenter = (0, 0)

    def __init__(self):
        super().__init__()
        self.mainscene = QGraphicsScene()
        self.mainscene.setSceneRect(0, 0, self.sw, self.sh)
        self.mainscene.addText("起点")
        self.initUI()
        self.mapview.init()
        self.mainview.init()

        self.timer = QTimer(self)
        self.timer.start(10)

    #初始化控件
    def initUI(self):
        self.resize(978, 594)
        centralWidget = QWidget(self)
        centralWidget.setObjectName('centralWidget')
        self.setCentralWidget(centralWidget)
        self.mainview = MainView(centralWidget) #大地图
        self.mainview.setGeometry(10, 10, 651, 511) #位置，大小

        self.mapview = MapView(centralWidget) #小地图
        self.mapview.setGeometry(670, 10, 301, 211)

        buttomview = QGraphicsView(centralWidget)
        buttomview.setGeometry(670, 270, 301, 211)

        self.text_edit = QLineEdit(centralWidget) #显示内容的文本框
        self.text_edit.setGeometry(670,490, 301, 27)

        self.text_input = QLineEdit(centralWidget)  # 显示内容的文本框
        self.text_input.setGeometry(10, 524, 301, 27)

        self.btn_save = QPushButton('保存',centralWidget)
        self.btn_save.setGeometry(QRect(670, 230, 80, 27))
        self.btn_load = QPushButton('加载', centralWidget)
        self.btn_load.setGeometry(QRect(780, 230, 80, 27))
        self.btn_save.clicked.connect(self.fileSave)
        self.btn_load.clicked.connect(self.fileLoad)

    #保存地图上的单位
    def fileSave(self):
        with open("filesave.txt", "w") as f:
            for key, value in self.mainview.dict_save.items():
                print(key, value)
                f.write('{}\t{}\n'.format(key, value))
            f.close()

    #加载保存的单位
    def fileLoad(self):
        with open("filesave.txt", "r") as f:
            line = f.readline()
            while line:
                load = line.split()
                for i in range(len(load)):
                    load[i] = load[i].strip('[')
                    load[i] = load[i].strip(',')
                    load[i] = load[i].strip(']')
                load[0] = load[0][:-2]
                #在地图中生成
                if load[0] == 'enemy_1':
                    enemy_1 = enemy_resource(timer=self.timer)
                    enemy_1.type = '1'
                    temp = self.mainview.mapToScene(int(load[1]), int(load[2]))
                    enemy_1.setBasePos(temp.x(), temp.y())
                    self.mainscene.addItem(enemy_1)
                elif load[0] == 'enemy_2':
                    enemy_2 = enemy_resource_1(timer=self.timer)
                    enemy_2.type = '2'
                    temp = self.mainview.mapToScene(int(load[1]), int(load[2]))
                    enemy_2.setBasePos(temp.x(), temp.y())
                    self.mainscene.addItem(enemy_2)
                elif load[0] == 'combat_R':
                    combat_R = Attacker(timer=self.timer)
                    combat_R.type = 'R'
                    temp = self.mainview.mapToScene(int(load[1]), int(load[2]))
                    combat_R.setBasePos(temp.x(), temp.y())
                    self.mainscene.addItem(combat_R)
                elif load[0] == 'combat_T':
                    combat_T = Attacker(timer=self.timer)
                    combat_T.type = 'T'
                    temp = self.mainview.mapToScene(int(load[1]), int(load[2]))
                    combat_T.setBasePos(temp.x(), temp.y())
                    self.mainscene.addItem(combat_T)
                else:
                    combat_Y = Attacker(timer=self.timer)
                    combat_Y.type = 'Y'
                    temp = self.mainview.mapToScene(int(load[1]), int(load[2]))
                    combat_Y.setBasePos(temp.x(), temp.y())
                    self.mainscene.addItem(combat_Y)

                line = f.readline()
        f.close()

    #更新小地图聚焦点
    def updateMainView(self):
        self.mainview.centerOn(self.mainViewCenter)

#大地图
class MainView(QGraphicsView):
    scene = QGraphicsScene
    def __init__(self, parent = 0):
        super().__init__(parent)
        self.cur_x = 0 #鼠标移动所在的坐标点
        self.cur_y = 0

        self.dict_save = dict() #将保存的单位放在字典中
        self.enemy_num = 0 #保存个数
        self.combat_num = 0
        self.combat_connect = [] #
        self.move_combat = None #保存要移动的单位
        self.connected = False
        self.item = None

    #初始化场景
    def init(self):
        self.window = self.parentWidget().parentWidget()
        self.scene = self.window.mainscene
        self.setScene(self.scene)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.timer = QTimer(self)
        self.timer.start(10)

        QWidget.setMouseTracking(self,True) #是鼠标移动可以获取坐标

    #控制作战单位移动和攻击
    def mousePressEvent(self, event: QtGui.QMouseEvent):
        # 点击左键选中作战单位
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move_combat = self.itemAt(self.cur_x, self.cur_y)
            if type(self.move_combat).__name__ == 'Attacker':
                self.window.text_edit.setText("选中目标：combat_R")
                if self.move_combat.carType == 'T' and self.move_combat._brush == QBrush(Qt.yellow):
                    # if self.connected == True:
                    #     self.scene.removeItem(self.item)
                    #     self.connected = False
                    # if self.connected == False:
                    #     self.move_combat.setBrush(QBrush(Qt.red))
                    #     self.item = QGraphicsEllipseItem(-150,-150,300,300)
                    #     self.item.setPos(self.mapToScene(event.pos().x(),event.pos().y()))
                    #     self.scene.addItem(self.item)
                    #     self.item.setZValue(-1)
                    #     self.connected = True
                    #     self.window.text_edit.setText("显示附近通讯单位")
                    self.move_combat.statues = 1
                    self.move_combat.mainview = self

        #鼠标右键选中目标
        elif event.buttons() == QtCore.Qt.RightButton:
            if self.move_combat != None:
                # if self.move_combat.type == 'T':
                #     # self.move_combat.statues = 0
                #     if self.connected == True:
                #         # self.scene.removeItem(self.item)
                #         self.connected = False
                target = self.itemAt(event.pos().x(), event.pos().y())
                #若目标是空白区域则移动到该位置
                if target == None:
                    self.move_combat.aimPos = self.mapToScene(event.pos().x(), event.pos().y())
                    self.window.text_edit.setText("移动到坐标点：("+str(event.pos().x())+","+str(event.pos().y())+")")
                #若目标是敌方则攻击
                elif type(target).__name__ == 'enemy_resource' or type(target).__name__ == 'enemy_resource_1':
                    if self.move_combat.carType == 'R':
                        m = missile(timer=self.timer)
                        m.setPos(self.move_combat.pos().x(), self.move_combat.pos().y())
                        self.scene.addItem(m)
                        m.aim = target
                        m.mainview = self
                        m.target = target
                        self.window.text_edit.setText("攻击敌方目标")

    #鼠标移动获取坐标点
    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        self.cur_x = event.pos().x()
        self.cur_y = event.pos().y()

    #键盘点击生成对应单位
    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key_R:
            combat_R = Attacker(id=1,carType='R',name='combat_R_1',belong_id=1,timer=self.timer)
            combat_R.setPos(self.mapToScene(self.cur_x, self.cur_y)) #设置初始点
            # temp = self.mapToScene(self.cur_x, self.cur_y)
            # combat_R.setBasePos(temp.x(), temp.y())
            self.scene.addItem(combat_R) #在场景中添加单位
            self.window.text_edit.setText("生成作战单位：combat_R")
        elif event.key() == Qt.Key_T:
            combat_T = Attacker(id=2, carType='T', name='combat_T_2', belong_id=1, timer=self.timer)
            combat_T.setPos(self.mapToScene(self.cur_x, self.cur_y))  # 设置初始点
            # temp = self.mapToScene(self.cur_x, self.cur_y)
            # combat_R.setBasePos(temp.x(), temp.y())
            self.scene.addItem(combat_T)  # 在场景中添加单位
            self.window.text_edit.setText("生成作战单位：combat_T")
        elif event.key() == Qt.Key_1:
            enemy_1 = enemy_resource(timer=self.timer)
            enemy_1.type = '1'
            temp = self.mapToScene(self.cur_x, self.cur_y)
            enemy_1.setBasePos(temp.x(), temp.y())
            self.scene.addItem(enemy_1)

            self.dict_save['enemy_1_' + str(self.enemy_num)] = [self.cur_x,self.cur_y]
            self.enemy_num += 1
            self.window.text_edit.setText("生成敌方单位：enemy_1")
        elif event.key() == Qt.Key_2:
            enemy_2 = enemy_resource_1(timer = self.timer)
            enemy_2.type = '2'
            temp = self.mapToScene(self.cur_x, self.cur_y)
            enemy_2.setBasePos(temp.x(), temp.y())
            self.scene.addItem(enemy_2)

            self.dict_save['enemy_2_' + str(self.enemy_num)] = [self.cur_x,self.cur_y]
            self.enemy_num += 1
            self.window.text_edit.setText("生成敌方单位：enemy_2")
        else:
            return

#小地图
class MapView(QGraphicsView):

    def __init__(self, parent=0):
        super().__init__(parent)

    def init(self):
        self.window = self.parentWidget().parentWidget()
        self.scene = self.window.mainscene
        self.setScene(self.scene)

        w = self.geometry().width()
        h = self.geometry().height()
        a = self.mapToScene(0, 0)
        b = self.mapToScene(w, h)

        sx = w / self.window.sw
        sy = h / self.window.sh
        print(w, h, a, b, sx, sy)
        self.scale(sx*0.95, sy*0.95)

    #鼠标点击要聚焦的位置
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.window.mainViewCenter = self.mapToScene(event.pos())
        self.window.updateMainView()
















