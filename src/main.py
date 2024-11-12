import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Widget(QWidget):

    def __init__(self, *args, **kwargs):
        self.data_orig= []    
        QWidget.__init__(self, *args, **kwargs)
        self.setWindowTitle("Хранилище документов")
        self.setAutoFillBackground(True)
        self.resize(1000,800); 

        layout1 = QGridLayout()
        self.edit1 = QLineEdit()
        
                       
        button1 =QPushButton("Укажите файл для загрузки")
        self.logwindow = QListWidget()
        layout1.addWidget(button1, 2, 1,1,1)
        layout1.addWidget(self.edit1, 3, 1,1,1)
        layout1.addWidget(self.logwindow, 4, 1,1,1)
        button1.clicked.connect(self.pickfile)
        self.setLayout(layout1)

    def pickfile(self):
        pickedfile, pickettype = QFileDialog.getOpenFileName(self, 'Укажите файл для загрузки', '')
        if pickedfile:
            self.edit1.setText(pickedfile)
            self.logwindow.addItem("Обработка файла {}".format(pickedfile))

if __name__ == "__main__":
   
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
