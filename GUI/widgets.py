from PyQt5.QtWidgets import *

class RightSideWidget(QWidget):
    def __init__(self, parent=None):
        super(RightSideWidget, self).__init__(parent)
        self.setFixedWidth(325)
        verticalLayout = QFormLayout()
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
        verticallayout = QVBoxLayout()
        headerlayout = QHBoxLayout()
        tabLayout = QHBoxLayout()
        self.leftside = None
        self.rightside = None
        self.initUI(tabLayout)
        self.initHeader(headerlayout)
        verticallayout.addLayout(headerlayout)
        verticallayout.addLayout(tabLayout)
        self.setLayout(verticallayout)

    def initHeader(self, headerlayout):
        pass
    def initUI(self,layout):
        pass
