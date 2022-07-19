from unicodedata import name
import timer
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QObject, QTimer, QPointF, QMetaObject, QRect
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QWidget, QGraphicsView, QPushButton, QTextEdit
from PyQt5.QtGui import QBrush, QPen, QPainter, QColor
from combat_resource import CombatResource
from enemy_resource import EnemyResource
import handle_process 
from log import log

class MainWindow(QMainWindow):
    sw = 1600; sh = 1200
    mainViewCenter = (0, 0)

    def __init__(self):
        super().__init__()
        self.mainscene = QGraphicsScene()
        self.mainscene.setSceneRect(0, 0, self.sw, self.sh)
        self.mainscene.addText("起点")
        self.initUI()
        self.mainview.init()

    def initUI(self):
        self.resize(2000, 1000) # 整体界面大小
        self.centralWidget = QWidget(self)
        self.centralWidget.setObjectName('centralWidget')
        
        self.setCentralWidget(self.centralWidget)
        
        # 一个框 （图片显示）
        self.mainview = MainView(self.centralWidget)
        self.mainview.setGeometry(10, 10, 1650, 800) # 边界

        # 输入框 （文字输入）
        self.textEdit = QTextEdit(self.centralWidget)
        self.textEdit.setGeometry(QRect(1670, 10, 290, 211))
        self.textEdit.setObjectName("textEdit")

        # 输出框 （文字显示）
        self.textOutput = QTextEdit(self.centralWidget)
        self.textOutput.setGeometry(1670, 270, 290, 530)
        self.textOutput.setObjectName("textOutput")
        
        # 日志输出框 （文字显示）
        self.logOutput = QTextEdit(self.centralWidget)
        self.logOutput.setGeometry(10, 820, 2000, 160)
        self.logOutput.setObjectName("logOutput")

        # 按钮
        self.btn_save = QPushButton('分析',self.centralWidget)
        self.btn_save.setGeometry(QRect(1670, 230, 80, 27))
        self.btn_save.clicked.connect(self.main_handle_process) # 产生什么事件

    def main_handle_process(self):
        """主要处理过程，处理输入 + 搜索计算 + 得到输出 + 渲染结果至 UI 
        """
        log.info("正在开始，清空白板......")
        self.mainscene.clear()
        self.centralWidget = None
    
        log.info("正在获取输入框文本......")
        inputStr = self.textEdit.toPlainText()

        log.info("正在分析处理输入数据 data: %s......" % inputStr)
        handler = handle_process.InputProcess(inputStr) 
        output, combat_map, enemy_map, final_hit_map = handler.main_process()
        
        log.info("正在输出结果......")
        self.insertOutputText(output)

        log.info("正在渲染 UI......")
        self.mainview.draw_items(combat_map, enemy_map, final_hit_map)
        
        log.info("########################################## END ##########################################\n\n")
      
    def insertOutputText(self, output):
        """输出结果至输出框
        """
        self.textOutput.clear()
        self.textOutput.insertPlainText(output)

#大地图
class MainView(QGraphicsView):
    scene = QGraphicsScene
    def __init__(self, parent = 0):
        super().__init__(parent)

    #初始化场景
    def init(self):
        self.window = self.parentWidget().parentWidget()
        self.scene = self.window.mainscene
        self.setScene(self.scene)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def draw_items(self, combat_map, enemy_map, hit_idx_map):
        """根据输入，画 item 至 UI 界面
        """
        log.info("draw_items: {} {} {}".format(combat_map, enemy_map, hit_idx_map))
        for key, value in hit_idx_map.items():
            combat_idx = combat_map["name"].index(key) # idx 对应的谁？
            enemy_idx = enemy_map["name"].index(value)
            
            # get cordinate
            combat_cordinate = (combat_map["x"][combat_idx], combat_map["y"][combat_idx])
            enemy_cordinate = (enemy_map["x"][enemy_idx], enemy_map["y"][enemy_idx])
            
            # create item
            temp_combat = CombatResource(id=1, 
                                         resource_type='R', 
                                         name=combat_map["name"][combat_idx],
                                         coordinate=combat_cordinate,
                                         value=0.5
                                         )
            log.info("combat_cordinate: {}".format(combat_cordinate))
            temp_combat.setPos(self.mapToScene(int(combat_cordinate[0]), int(combat_cordinate[1])))  # 设置初始点
            self.scene.addItem(temp_combat)  # 在场景中添加单位
            # self.window.text_edit.setText("生成作战单位：")
            
            temp_enemy = EnemyResource(id=1, 
                                       resource_type='R', 
                                       name=enemy_map["name"][enemy_idx],
                                       coordinate=combat_cordinate,
                                         value=0.5)
            log.info("enemy_cordinate: {}".format(enemy_cordinate))
            temp_enemy.setPos(self.mapToScene(int(enemy_cordinate[0]), int(enemy_cordinate[1])))  # 设置初始点
            self.scene.addItem(temp_enemy)  # 在场景中添加单位
            # # self.window.text_edit.setText("生成作战单位：")

            self._command_attack(temp_combat, temp_enemy)
            
    def _command_attack(self, combat, target):
        '''打击连线
        '''
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        self.scene.addLine(combat.pos().x(), combat.pos().y(), target.pos().x(), target.pos().y(),pen)
        # self.window.text_edit.setText("攻击敌方目标")
