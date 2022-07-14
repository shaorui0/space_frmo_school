import timer
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QObject, QTimer, QPointF, QMetaObject, QRect
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QWidget, QGraphicsView, QPushButton, QTextEdit

from combat_resource import Attacker
from enemy_resource import enemy_resource, enemy_resource_1

import inputProcess 

class MainWindow(QMainWindow):

    sw = 1600; sh = 1200
    mainViewCenter = (0, 0)

    def __init__(self):
        super().__init__()
        self.mainscene = QGraphicsScene()
        self.mainscene.setSceneRect(0, 0, self.sw, self.sh)
        self.mainscene.addText("起点")
        self.initUI()
        # self.mapview.init() // TODO 输入框
        self.mainview.init()

    def initUI(self):
        self.resize(1000, 800) # 整体界面大小
        centralWidget = QWidget(self)
        centralWidget.setObjectName('centralWidget')
        self.setCentralWidget(centralWidget)
        
        # 一个框 （图片显示）
        self.mainview = MainView(centralWidget)
        self.mainview.setGeometry(10, 10, 650, 780) # 边界

        # 输入框 （文字输入）
        self.textEdit = QTextEdit(centralWidget)
        self.textEdit.setGeometry(QRect(670, 10, 301, 211))
        self.textEdit.setObjectName("textEdit")

        # 输出框 （文字显示）
        self.textOutput = QTextEdit(centralWidget)
        self.textOutput.setGeometry(670, 270, 301, 500)
        self.textOutput.setObjectName("textOutput")

        # 按钮
        self.btn_save = QPushButton('分析',centralWidget)
        self.btn_save.setGeometry(QRect(670, 230, 80, 27))
        self.btn_save.clicked.connect(self.handle_input) # 产生什么事件

    def handle_input(self):
        # 获取输入框文本
        inputStr = self.textEdit.toPlainText()

        # 处理输入，得到输出
        pros = inputProcess.InputProcess(inputStr) 
        output = pros.main_process()
        
        # 输出结果
        self.printOutputText(output)

        # TODO 渲染 mainView


    def printOutputText(self, output):
        self.textOutput.clear()
        self.textOutput.insertPlainText(output)


class MainView(QGraphicsView):

    scene = QGraphicsScene
    def __init__(self, parent = 0):
        super().__init__(parent)
        self.cur_x = 0
        self.cur_y = 0

        self.dict_save = dict()
        self.enemy_num = 0
        self.combat_num = 0
        self.list_combat = []

    def init(self):
        self.window = self.parentWidget().parentWidget()
        self.scene = self.window.mainscene
        self.setScene(self.scene)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.timer = QTimer(self)
        self.timer.start(10)

