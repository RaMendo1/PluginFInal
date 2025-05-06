import maya.cmds as mc 
import maya.OpenMayaUI as omui 
import shiboken2 
import maya.mel as mel
from maya.OpenMaya import MVector

from PySide2.QtWidgets import (QLineEdit, 
                               QListWidget, 
                               QMainWindow, 
                               QMessageBox, 
                               QWidget, 
                               QVBoxLayout, 
                               QHBoxLayout, 
                               QLabel, 
                               QSlider, 
                               QPushButton)
from PySide2.QtCore import Qt

from MayaUtils import QMayaWindow

class FingerJntManager:
    def __init__(self, parent=None):
        self.leftControls = []
        self.rightControls = []
        self.parent = parent

    def addToLeftList(self, items):
        self.leftControls.extend(items)

    def addToRightList(self, items):
        self.rightControls.extend(items)

    def clearLeftList(self):
        self.leftControls = []
    
    def clearRightList(self):
        self.rightControls = []

    def resetLeftFingers(self):
        if not self.leftControls:
            QMessageBox.warning(self.parent, "Error", "Left hand list is empty.")
            return
        for ctrl in self.leftControls:
            if mc.objExists(ctrl):
                mc.setAttr(ctrl + ".rotate", 0, 0, 0)

    def resetRightFingers(self):
        if not self.rightControls:
            QMessageBox.warning(self.parent, "Error", "Right hand list is empty.")
            return
        for ctrl in self.rightControls:
            if mc.objExists(ctrl):
                mc.setAttr(ctrl + ".rotate", 0, 0, 0)

    def selectLeftFingers(self):
        if not self.leftControls:
            QMessageBox.warning(self.parent, "Error", "Left hand list is empty.")
            return
        mc.select(self.leftControls, replace=True)

    def selectRightFingers(self):
        if not self.rightControls:
            QMessageBox.warning(self.parent, "Error", "Right hand list is empty.")
            return
        mc.select(self.rightControls, replace=True)

class FingerJntToolWidget(QMayaWindow):
    def __init__(self): 
        super().__init__()
        self.setWindowTitle("FingerJntManager") 
        self.manager = FingerJntManager(parent=self)
        self.ToolUI()

    def ToolUI(self):
        masterLayout = QVBoxLayout()

        # === LEFT HAND SECTION ===
        self.leftListWidget = QListWidget()
        leftTitle = QLabel("Left Hand Selection")
        addLeftBtn = QPushButton("Add Selected to Left Hand List")
        addLeftBtn.clicked.connect(self.addSelectedToLeft)
        
        clearLeftBtn = QPushButton("Clear Left Hand List")
        clearLeftBtn.clicked.connect(self.clearLeftUIList)

        masterLayout.addWidget(leftTitle)
        masterLayout.addWidget(self.leftListWidget)
        masterLayout.addWidget(addLeftBtn)
        masterLayout.addWidget(clearLeftBtn)

        # === RIGHT HAND SECTION ===
        masterLayout.addSpacing(20)
        self.rightListWidget = QListWidget()
        RightTitle = QLabel("Right Hand Selection")
        addRightBtn = QPushButton("Add Selected to Right Hand List")
        addRightBtn.clicked.connect(self.addSelectedToRight)

        clearRightBtn = QPushButton("Clear Right Hand List")
        clearRightBtn.clicked.connect(self.clearRightUIList)

        masterLayout.addWidget(RightTitle)
        masterLayout.addWidget(self.rightListWidget)
        masterLayout.addWidget(addRightBtn)
        masterLayout.addWidget(clearRightBtn)

        # === CONTROL BUTTONS ===
        masterLayout.addSpacing(20)
        selectLeftBtn = QPushButton("Select All Left Fingers")
        selectRightBtn = QPushButton("Select All Right Fingers")
        resetLeftBtn = QPushButton("Reset Left Rotations")
        resetRightBtn = QPushButton("Reset Right Rotations")

        selectLeftBtn.clicked.connect(self.manager.selectLeftFingers)
        selectRightBtn.clicked.connect(self.manager.selectRightFingers)
        resetLeftBtn.clicked.connect(self.manager.resetLeftFingers)
        resetRightBtn.clicked.connect(self.manager.resetRightFingers)

        masterLayout.addWidget(selectLeftBtn)
        masterLayout.addWidget(selectRightBtn)
        masterLayout.addWidget(resetLeftBtn)
        masterLayout.addWidget(resetRightBtn)

        self.setLayout(masterLayout)

    def addSelectedToLeft(self):
        sel = mc.ls(selection=True)
        if not sel:
            return

        rightItems = self.getListWidgetItems(self.rightListWidget)
        validItems = [item for item in sel if item not in rightItems]

        if not validItems:
            QMessageBox.warning(self, "Warning", "Some or all selected items are already in the Right Hand List.")
            return

        self.manager.addToLeftList(validItems)
        for item in validItems:
            if item not in self.getListWidgetItems(self.leftListWidget):
                self.leftListWidget.addItem(item)

    def addSelectedToRight(self):
        sel = mc.ls(selection=True)
        if not sel:
            return

        left_items = self.getListWidgetItems(self.leftListWidget)
        validItems = [item for item in sel if item not in left_items]

        if not validItems:
            QMessageBox.warning(self, "Warning", "Some or all selected items are already in the Left Hand List.")
            return

        self.manager.addToRightList(validItems)
        for item in validItems:
            if item not in self.getListWidgetItems(self.rightListWidget):
                self.rightListWidget.addItem(item)

    def getListWidgetItems(self, listWidget):
        return [listWidget.item(i).text() for i in range(listWidget.count())]
    
    def clearLeftUIList(self):
        self.leftListWidget.clear()
        self.manager.clearLeftList()

    def clearRightUIList(self):
        self.rightListWidget.clear()
        self.manager.clearRightList()

def Run():
    FingerJntToolWidget().show()