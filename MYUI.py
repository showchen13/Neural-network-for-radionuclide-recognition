from PyQt5.QtWidgets import QStyleFactory
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from matplotlib.lines import Line2D
from PyQt5.QtWidgets import QApplication,QMainWindow,QGridLayout
from UI2 import *
from tkinter import filedialog
import data_load
from PyQt5.QtWidgets import QMainWindow,QApplication,QTextEdit,QAction,QFileDialog
import matplotlib.pyplot as plt
from PyQt5.QtCore import pyqtSlot

class Figure_Canvas(FigureCanvas):
    def __init__(self,parent=None,width=3.9,height=2.7,dpi=100):
        self.fig=Figure(figsize=(width,height),dpi=100)
        super(Figure_Canvas,self).__init__(self.fig)
        self.ax=self.fig.add_subplot(111)



class MyPyQT_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyPyQT_Form,self).__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.Button)
        self.pushButton_2.clicked.connect(self.Button_select)
        self.inifui()


    def inifui(self):


        label, data_list = data_load.predict('data/7/20200108173658596_201A8110.spe')
        label2, data_list2 = data_load.predict('data/7/20200108173658596_201A8110.spe')
        self.x = range(0, len(data_list))
        self.z = data_list
        self.y = data_list2

        self.LineFigure = Figure_Canvas()
        self.LineFigureLayout = QGridLayout(self.groupBox)
        self.LineFigureLayout.addWidget(self.LineFigure)
        self.LineFigure.ax.set_xlim(0, 2048)
        self.LineFigure.ax.set_ylim(0, 1500)
        self.line = Line2D(self.x, self.z, color='red')
        self.line2 = Line2D(self.x, self.y, color='green')
        self.LineFigure.ax.add_line(self.line2)
        # self.LineFigure.ax.remove(self.line[0])

        self.LineFigure.ax.add_line(self.line)
        self.label.setText(label)
        # self.LineFigure.ax.plot(self.x, self.z)



    # @pyqtSlot()
    def Button_select(self):


        self.module_dir = QFileDialog.getOpenFileName(self,'open file', '/', "pth files (*.pth)")
        if self.module_dir[0] == '':
            return
        print(self.module_dir[0])

    def Button(self):


        data_dir = QFileDialog.getOpenFileName(self, 'open file', '/', "spe files (*.spe)")

        if data_dir[0] == '':
            return
        print(data_dir)
        label, data_list = data_load.predict(data_dir[0])
        self.LineFigure.ax.set_xlim(0, 2048)
        self.LineFigure.ax.set_ylim(0, max(data_list) + 500)
        self.line.set_ydata(data_list)
        self.LineFigure.draw()



        self.label.setText(label)



        '''
        能谱可视化
        
        
        '''



        # plt.ylabel('cps')
        # plt.xlabel('ch')
        # plt.plot(range(0, len(data_list)), data_list)
        # plt.show()

        # print(label)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # The available styles depend on your platform
    # but are usually 'Fusion', 'Windows', 'WindowsVista' (Windows only)
    # and 'Macintosh' (Mac only).
    app.setStyle(QStyleFactory.create('Fusion'))
    my_pyqt_form = MyPyQT_Form()
    # my_pyqt_form = Ui_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())