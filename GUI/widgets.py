from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout)

class RightSideWidget(QWidget):
    def __init__(self, parent=None):
        super(RightSideWidget, self).__init__(parent)
        self.setFixedWidth(250)
        verticalLayout = QVBoxLayout()
        self.initUI(verticalLayout)
        self.setLayout(verticalLayout)

    def initUI(self, layout):
        label = QLabel()
        label.setText("Right side")
        layout.addWidget(label)

class LeftSideWidget(QWidget):
    def __init__(self, parent=None):
        super(LeftSideWidget, self).__init__(parent)
        self.setMinimumWidth(450)
        self.setMaximumWidth(750)
        verticalLayout = QVBoxLayout()
        self.initUI(verticalLayout)
        self.setLayout(verticalLayout)

    def initUI(self, layout):
        label = QLabel()
        label.setText("Left side")
        layout.addWidget(label)

class TabWidget(QWidget):
    def __init__(self,parent=None):
        super(TabWidget, self).__init__(parent)
        tabLayout = QHBoxLayout()
        self.leftside = None
        self.rightside = None
        self.initUI(tabLayout)
        self.setLayout(tabLayout)

    def initUI(self,layout):
        pass
