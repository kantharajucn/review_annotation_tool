from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import pandas as pd
import csv
import os
import time
from PyQt5.QtWidgets import QWidget


class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.counter = 1
        self.df = None
        self.flag = 0
        self.completed = 0
        
    def initUI(self):
        self.setWindowTitle("Annotation")
        self.resize(800, 600)
        self.hlayout1 = QtWidgets.QGridLayout()
        self.title = QtWidgets.QLabel("Annotation Tool")
        self.title.setFont(QtGui.QFont('Arial', 20))
        self.type = QtWidgets.QLabel("Annotation for")
        self.type_select = QtWidgets.QComboBox()
        self.type_select.addItems(["Helpfulness","Spam"])
        self.progress = QtWidgets.QLabel("Annotation Progress")
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setProperty("value", 0)
        self.rid = QtWidgets.QLabel("Review ID")
        self.rid_edit = QtWidgets.QLineEdit()
        self.rid_edit.setFont(QtGui.QFont('Arial', 13))
        self.rtitle = QtWidgets.QLabel("Review Title")
        self.rtitle_edit = QtWidgets.QLineEdit()
        self.rtitle_edit.setFont(QtGui.QFont('Arial', 14))
        self.rtext = QtWidgets.QLabel("Review")
        self.rtext_edit = QtWidgets.QTextEdit()
        self.rtext_edit.setFont(QtGui.QFont('Arial', 16))
        self.label_4 = QtWidgets.QLabel()
        self.prev = QtWidgets.QPushButton("Prev")
        self.next = QtWidgets.QPushButton("Next")
        self.start = QtWidgets.QDialogButtonBox()
        self.start.addButton("Start tool", QtWidgets.QDialogButtonBox.AcceptRole)
        self.start.addButton("Stop tool", QtWidgets.QDialogButtonBox.RejectRole)
        self.start.layout().setDirection(QtWidgets.QBoxLayout.LeftToRight)
        self.vote = QtWidgets.QLabel("User Rating")
        self.helpful = QtWidgets.QComboBox()
        nums = [str(i) for i in range(1,101)]
        self.helpful.addItems(nums)
        self.spam = QtWidgets.QComboBox()
        self.spam.addItems(["Spam","Non Spam"])
        
        self.hlayout1.addWidget(self.title,0,0,1,3,QtCore.Qt.AlignCenter)
        self.hlayout1.addWidget(self.type,1,0)
        self.hlayout1.addWidget(self.type_select,1,1)
        self.hlayout1.addWidget(self.progress,2,0)
        self.hlayout1.addWidget(self.progressBar,2,1)
        self.hlayout1.addWidget(self.rid,3,0)
        self.hlayout1.addWidget(self.rid_edit,3,1)
        self.hlayout1.addWidget(self.rtitle,4,0)
        self.hlayout1.addWidget(self.rtitle_edit,4,1)
        self.hlayout1.addWidget(self.rtext,5,0)
        self.hlayout1.addWidget(self.rtext_edit,5,1)
        self.hlayout1.addWidget(self.helpful,5,2)
        self.hlayout1.addWidget(self.spam,5,3)
        self.hlayout1.addWidget(self.next,6,0,1,2,QtCore.Qt.AlignRight)
        self.hlayout1.addWidget(self.prev,6,1,1,2,QtCore.Qt.AlignLeft)
        self.hlayout1.addWidget(self.start,7,0,1,3,QtCore.Qt.AlignCenter)
        self.setLayout(self.hlayout1)
        self.start.accepted.connect(self.startAnnotation)
        self.start.rejected.connect(self.stopAnnotation)
        self.prev.clicked.connect(self.decrement)
        self.next.clicked.connect(self.increment)
    
    def startAnnotation(self):
        print("Annotation is started")
        self.start_time =time.time()
        df = pd.read_csv('validation.csv')
        if self.type_select.currentText() == 'Helpfulness':
            self.spam.setEnabled(False)
            self.helpful.setEnabled(True)
            self.flag = 0
        else:
            self.helpful.setEnabled(False)
            self.spam.setEnabled(True)
            self.flag = 1
        self.df = df
        self.annotate()
    def annotate(self):
        row = self.df.iloc[self.counter]
        self.rid_edit.setText(row[0])
        self.rtitle_edit.setText(row[1])
        self.rtext_edit.setText(row[2])
        
        if self.flag == 0:
            with open('annotation_helpful.csv','a+',newline='') as csv_file:
                writer = csv.writer(csv_file)
                text = [row[0],row[1],self.helpful.currentText()]
                writer.writerow(text)
        else:
            with open('annotation_spam.csv','a+',newline='') as csv_file:
                writer = csv.writer(csv_file)
                text = [row[0],row[1],self.helpful.currentText()]
                writer.writerow(text)
    def increment(self):
        self.counter +=1
        
        if self.completed < 100:
            self.completed = (self.counter/len(self.df.index))*100
        self.progressBar.setValue(self.completed)    
        self.annotate() 
    
    def decrement(self):
        if self.counter == 1:
            self.counter = 1
        else:
            self.counter -= 1  
        if self.completed < 100:
            self.completed -= 0.1     
        (self.counter/len(self.df.index))*100
        self.annotate() 
 
    def stopAnnotation(self):
        self.end_time =time.time()
        self.elapsed  = self.end_time - self.start_time
        print("Annotation is completed")
        print("Time taken to finish the annotation:{0} Mins".format(self.elapsed))
        self.close()

        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    prog = MyApp()
    prog.show()
    sys.exit(app.exec_())