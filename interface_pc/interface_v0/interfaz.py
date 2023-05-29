
from PyQt5.QtWidgets import *  
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from UI_design import *



class UI_MainWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(UI_MainWindow,self).__init__(*args,**kwargs)
        setupUi(self)


    # def retranslateUi(self, QMainWindow):


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ui = UI_MainWindow()
    ui.show()
    sys.exit(app.exec_())
