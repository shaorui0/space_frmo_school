import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileSystemModel, QFileIconProvider, QApplication,\
    QTreeView
    
class FileIconProvider(QFileIconProvider):
 
    def __init__(self, *args, **kwargs):
        super(FileIconProvider, self).__init__(*args, **kwargs)
        self.DirIcon = QIcon("C:\Users\rshao\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu20.04onWindows_79rhkp1fndgsc\LocalState\rootfs\home\rshao\.local\lib\python3.8\site-packages\PyQt5\Qt5\qml\QtQuick\Controls.2\designer\images\label-icon@2x.png")
        
 
    def icon(self, type_info):
        if isinstance(type_info, QFileInfo):
            return self.getInfoIcon(type_info)
 
        if type_info == QFileIconProvider.Folder:
            # 如果是文件夹
            return self.DirIcon
        return super(FileIconProvider, self).icon(type_info)
 
    def getInfoIcon(self, type_info):
        if type_info.isDir():  # 文件夹
            return self.DirIcon
        return super(FileIconProvider, self).icon(type_info)