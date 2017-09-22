from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import pandas as pd
import csv
import os
import time
import os, glob
from PyQt5.QtWidgets import QWidget


class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.counter = 0
        self.df = None
        self.flag = 0
        self.completed = 0
        
    def initUI(self):
        self.setWindowTitle("Annotation")
        self.resize(800, 600)
        self.hlayout1 = QtWidgets.QGridLayout()
        self.title = QtWidgets.QLabel("Annotation Tool")
        self.title.setFont(QtGui.QFont('Arial', 20))
        self.type = QtWidgets.QLabel("Annotation type")
        self.type_select = QtWidgets.QComboBox()
        self.type_select.addItems(["Sequential","Random"])
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
        nums = ["--HELPFULNESS--","0","1","2","3","4","5","6","7","8","9","10"]
        self.helpful.addItems(nums)
        self.spam = QtWidgets.QComboBox()
        self.spam.addItems(["--SPAM--","Spam","Non-spam"])
        
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
        for filename in glob.glob("./annotation*.csv"):
            new_file = filename + "." + str(self.start_time)
            os.rename(filename,new_file)
        df = pd.read_csv('validation.csv')
        if self.type_select.currentText() == "Sequential":
            self.filename = "annotation_sequential.csv"
            df = df
        else:
            self.filename = "annotation_random.csv"
            df = df.sample(frac=1)
        self.df = df
        self.annotate()
    def annotate(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        if self.counter == 24:
            msg.setText("You have completed 25 reviews take rest for 5 minutes")
            msg.exec_()
            self.end_time = time.time()
            self.elapsed = self.end_time - self.start_time
            print("Time taken to finish 1-25:{0} Seconds".format(self.elapsed))
            self.next.setEnabled(False)
            time.sleep(300)
            msg.setText("Resume annotation")
            msg.exec_()
            self.next.setEnabled(True)
            self.start_time = time.time()
        if self.counter == 49:
            msg.setText("You have completed 50 reviews take rest for 5 minutes")
            msg.exec_()
            self.end_time = time.time()
            self.elapsed = self.end_time - self.start_time
            print("Time taken to finish 25-50:{0} Seconds".format(self.elapsed))
            self.next.setEnabled(False)
            time.sleep(300)
            msg.setText("Resume annotation")
            msg.exec_()
            self.next.setEnabled(True)
            self.start_time = time.time()
        if self.counter == 74:
            msg.setText("YOu have completed 75 reviews take rest for 5 minutes")
            msg.exec_()
            self.end_time = time.time()
            self.elapsed = self.end_time - self.start_time
            print("Time taken to finish 50-75:{0} Seconds".format(self.elapsed))
            self.next.setEnabled(False)
            time.sleep(300)
            msg.setText("Resume annotation")
            msg.exec_()
            self.next.setEnabled(True)
            self.start_time = time.time()
        if self.counter == 99:
            msg.setText("You have finished all reviews")
            msg.exec_()
            self.end_time = time.time()
            self.elapsed = self.end_time - self.start_time
            print("Time taken to finish 75-100:{0} Seconds".format(self.elapsed))

            return 0
        self.row = self.df.iloc[self.counter]
        self.rid_edit.setText(self.row[0])
        self.rtitle_edit.setText(self.row[1])
        self.rtext_edit.setText(self.row[2])

    def increment(self):
        self.counter +=1
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        if self.completed < 100:
            self.completed = (self.counter/len(self.df.index))*100
        self.progressBar.setValue(self.completed)

        with open(self.filename,'a+',newline='') as csv_file:
            writer = csv.writer(csv_file)
            text = [self.row[0],self.row[1],self.helpful.currentText(),self.spam.currentText()]
            writer.writerow(text)
        self.helpful.setCurrentText("--HELPFULNESS--") 
        self.spam.setCurrentText("--SPAM--")  
        self.annotate() 
    
    def decrement(self):
        if self.counter == 1:
            self.counter = 1
        else:
            self.counter -= 1  
        if self.completed < 100:
            self.completed -= 0.1     
        (self.counter/len(self.df.index))*100
        with open(self.filename,'a+',newline='') as csv_file:
            writer = csv.writer(csv_file)
            text = [self.row[0],self.row[1],self.helpful.currentText(),self.spam.currentText()]
            writer.writerow(text)
        self.helpful.setCurrentText("--HELPFULNESS--") 
        self.spam.setCurrentText("--SPAM--") 
        self.annotate() 
 
    def stopAnnotation(self):
        self.end_time =time.time()
        self.elapsed  = self.end_time - self.start_time
        print("Annotation is completed")
        print("Time taken to finish the annotation:{0} Seconds".format(self.elapsed))
        self.close()

        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    prog = MyApp()
    prog.show()
    sys.exit(app.exec_())
