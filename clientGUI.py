'''
Data Logger V0.1 Demo  :: (GUI and Plotting)

Autour: Kamal Moussa
Created 5 Nov 2016
last Edit 10 Nov 2016

'''


import sys
import socket
import time

import numpy as np



import random

from PyQt4 import QtGui,QtCore

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

import matplotlib.pyplot as plt


begin = 0

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.toolbar_config()

        self.setGeometry(250, 200, 1500, 700)
        self.setMinimumSize(700, 700)
        self.setWindowTitle('Data Logger V 1.0')

        self.Logged_out()

    def toolbar_config(self):

        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        Snapshot = QtGui.QAction("&Snapshot", self)
        Snapshot.setShortcut("Ctrl+S")
        Snapshot.setStatusTip('Save File')
        Snapshot.triggered.connect(self.take_snapshot)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(Snapshot)
        fileMenu.addAction(exitAction)


    def take_snapshot(self):
        #widget = QWidget()
        p = QPixmap.grabWindow(self.winId())
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save Snapshot')
        p.save(name,'JPG')

    def file_save(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        file = open(name,'w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()



    def Logged_out(self):

        self.statusBar().showMessage('Ready to Connect')
        self.setCursor(Qt.WaitCursor)
        time.sleep(0.5)  # wait 0.5 second
        self.setCursor(Qt.ArrowCursor)

        self.login_W = loggingLayout()
        self.central_widget.addWidget(self.login_W)
        self.central_widget.setCurrentWidget(self.login_W)

        self.login_W.connectButton.clicked.connect(self.Logged_in)


    def Logged_in(self):

        self.statusBar().showMessage('Welcome')

        self.IP_address= self.login_W.lineEdit.text()

        self.logout_w = Data_log()

        if(self.logout_w.check_(str(self.IP_address))):
       # if(1):

            #self.logout_w.client_get_user(self.IP_address)
            self.central_widget.addWidget(self.logout_w)
            self.central_widget.setCurrentWidget(self.logout_w)
            self.logout_w.logoutButton.clicked.connect(self.logout_alert)
            self.logout_w.Update.clicked.connect(self.send_)

        else:
            self.Logged_out()


    def logout_alert(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText("Are you sure to end this session")
        msgBox.addButton(QtGui.QPushButton('Accept'), QtGui.QMessageBox.YesRole)
        msgBox.addButton(QtGui.QPushButton('Cancel'), QtGui.QMessageBox.RejectRole)
        ret = msgBox.exec_()
        if(not ret):
            self.if_yes()


    def if_yes(self):

        self.logout_w.close_()
        self.Logged_out()



    def send_(self):
        self.logout_w.client_send_message(self.IP_address)


class loggingLayout(QtGui.QWidget):
    def __init__(self, parent=None):
        super(loggingLayout, self).__init__(parent)
        self.initLayout()


    def initLayout(self):


        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(16)

        font2 = QtGui.QFont()
        font2.setPointSize(18)

        self.lineEdit= QtGui.QLineEdit()
        self.connectButton= QtGui.QPushButton("Connect")
        self.welcomeLabel = QtGui.QLabel()

        self.lineEdit.setMaximumWidth(250)
        self.lineEdit.setMinimumWidth(150)
        self.lineEdit.setFont(font2)
        self.lineEdit.setPlaceholderText("What IP, please?")


        self.connectButton.setMaximumWidth(350)
        self.connectButton.setMinimumWidth(150)
        self.connectButton.setFont(font)

        self.welcomeLabel.setText("Welcome to Your Data Logger")
        self.welcomeLabel.setFont(font2)
        self.welcomeLabel.setMinimumSize(300,100)

        hEbox = QtGui.QHBoxLayout()
        hEbox.addStretch()
        hEbox.addWidget(self.lineEdit)
        hEbox.addStretch()

        hBbox = QtGui.QHBoxLayout()        # hEbox.setContentsMargins(0, 0, 0, 0)

        hBbox.addStretch()
        hBbox.addWidget(self.connectButton)
        hBbox.addStretch()

        hLbox=QtGui.QHBoxLayout()
        hLbox.addStretch()
        hLbox.addWidget(self.welcomeLabel)
        hLbox.addStretch()

        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addStretch()
        self.vbox.addLayout(hLbox)
        self.vbox.addLayout(hEbox)
        self.vbox.addLayout(hBbox)
        self.vbox.addStretch()

        self.lineEdit.setStyleSheet("border-radius: 10px; border: 3px solid #BADA55; background: white;")
        self.connectButton.setStyleSheet("border-radius: 10px; background: #BADA55; width: 60px; height: 40px")
        self.welcomeLabel.setStyleSheet("border-radius: 10px; height: 40px;font-size: 200%;text-align: center;")

        self.setLayout(self.vbox)


class Data_log(QtGui.QWidget):

    # min_x = 0
    # max_x = 10
    t_counter =0

    def __init__(self):
        super(Data_log, self).__init__()
        self.initUI()


    def initUI(self):

        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(16)

        font2 = QtGui.QFont()
        font2.setPointSize(18)


        # self.lineEdit= QtGui.QLineEdit()
        self.logoutButton= QtGui.QPushButton("Log Out")
        self.Update= QtGui.QPushButton("Send Request")

        self.helloText =QtGui.QTextEdit()
        self.helloText.setReadOnly(True)

        self.logoutButton.setMaximumWidth(350)
        self.logoutButton.setMinimumWidth(150)
        self.logoutButton.setFont(font)

        self.Update.setMaximumWidth(350)
        self.Update.setMinimumWidth(200)
        self.Update.setFont(font)

        self.helloText.setMaximumWidth(500)
        self.helloText.setMinimumWidth(300)
        self.helloText.setMaximumHeight(100)
        self.helloText.setMinimumHeight(50)
        self.helloText.setFont(font)

        hBbox = QtGui.QHBoxLayout()
        hBbox.addStretch()
        hBbox.addWidget(self.logoutButton)
        hBbox.addWidget(self.Update)
        hBbox.addStretch()
        hBbox.setContentsMargins(0, 0, 0, 20)

        self.hTbox=QtGui.QHBoxLayout()
        self.hTbox.addStretch()
        self.hTbox.addWidget(self.helloText)
        self.hTbox.addStretch()
        self.hTbox.setContentsMargins(0,50,0,20)

        self.plot_config()

        #-------Graphs box-----------#
        self.hWbox = QtGui.QHBoxLayout()
        self.hWbox.addWidget(self.canvas1)
        self.hWbox.addWidget(self.canvas2)
        self.hWbox.addWidget(self.canvas3)
        self.hWbox.setContentsMargins(20,0,20,50)


        self.vbox = QtGui.QVBoxLayout()
        # self.vbox.addLayout(hEbox)
        self.vbox.addLayout(self.hTbox)
        self.vbox.addLayout(hBbox)
        self.vbox.addLayout(self.hWbox)

        #-----Stylesheets----#
        # self.lineEdit.setStyleSheet("border-radius: 10px; border: 3px solid #BADA55; background: white;")
        self.logoutButton.setStyleSheet("border-radius: 10px; background: #BADA55;  height: 40px")
        self.Update.setStyleSheet("border-radius: 10px; background: #BADA55; height: 40px")
        self.helloText.setStyleSheet("border-radius: 10px; border: 3px solid #BADA55; background: white;")

        self.setLayout(self.vbox)



        # self.logoutButton.clicked.connect(self.Exit_msg)


    def plot_config(self):
        self.fig1 = Figure()
        self.fig2 = Figure()
        self.fig3 = Figure()

        self.fig1.set_facecolor('white')
        self.fig2.set_facecolor('white')
        self.fig3.set_facecolor('white')

        self.canvas1 = FigureCanvas(self.fig1)
        self.canvas2 = FigureCanvas(self.fig2)
        self.canvas3 = FigureCanvas(self.fig3)


        self.tempPlot = self.fig1.add_subplot(111)
        self.PressPlot = self.fig2.add_subplot(111)
        self.AltPlot = self.fig3.add_subplot(111)


        self.tempPlot.set_axis_bgcolor((0.2, 0.2, 0.22))
        self.PressPlot.set_axis_bgcolor((0.2, 0.2, 0.22))
        self.AltPlot.set_axis_bgcolor((0.2, 0.2, 0.22))

        self.tempPlot.set_title('Temperature Log')
        self.tempPlot.set_xlabel('t (s)')
        self.tempPlot.set_ylabel('T (C)')

        self.PressPlot.set_title('Pressure Log')
        self.PressPlot.set_xlabel('t (s)')
        self.PressPlot.set_ylabel('P (hPa)')

        self.AltPlot.set_title('Altitude Log')
        self.AltPlot.set_xlabel('t (s)')
        self.AltPlot.set_ylabel('A (m)')


    def start_server(self,ip_address):


        # ip_address = '192.168.1.104'
        print (ip_address)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # msg_box("", "Socket Created")
        try:
            client.connect((ip_address, 80))

        except Exception, e:
            self.msg_box("Connection Refused", "The Address You Are Trying To Reach Is Currently Unavailable")
        return client

    def client_send_message(self,IP):
        #---plot test----#
        # T = 0
        # A = 0
        # P = 0
        # while True:
        #     self.start_plot(T, A, P)
        #     T += 1
        #     A += 1
        #     P += 1
        #     self.t_counter += 2
        #     time.sleep(1)

       # ----- Autour: Ahmed Atallah-------#

        self.client = self.start_server(IP)
        timeout = 2
        all_recv = {"User": "", "Temp": "", "Press": "", "Altit": "", "NoData Ind":""}
        begin = time.time()

        while True:
            try:
                self.client.send('GET')
            except:
                # msg_box("Broken pipe", "Your socket pipe closed")
                break

            # if you got no data at all, wait a little longer, twice the timeout
            if time.time() - begin > timeout * 2 and all_recv["NoData Ind"] == "oh":
                self.msg_box("time out", "time out no data recieved")
                print "time out"


            # recv something
            try:
                sensors_out = self.client.recvfrom(32)
                print sensors_out[0]

                if sensors_out[0] == "oh":
                    all_recv["NoData Ind"] = sensors_out[0]

                sensor_D = sensors_out[0].split(',')

                U=sensor_D[0]
                T=sensor_D[1]
                P=sensor_D[2]
                A=sensor_D[3]

                self.helloText.setText("Welcome,  "+ U)
                self.start_plot(A, T, P)
                self.t_counter+=1

                if sensors_out[0] != "":
                    all_recv['User']  +=  (sensor_D[0] + ',')
                    all_recv['Temp']  +=  (sensor_D[1] + ',')
                    all_recv['Press'] += (sensor_D[2] + ',')
                    all_recv['Altit'] += (sensor_D[3] + ',')

                    # change the beginning time for measurement
                    begin = time.time()

                else:
                  time.sleep(0.1)

            except:
                pass

        print all_recv
        self.client.close()

    def close_(self):
        self.client.close()


    # def client_get_user(self, IP):
    #     print 'client get user'
    #     self.helloText.setText(str(IP))
        #
        # client = self.start_server(IP)
        #
        # all_recv = {"User": " "}
        #
        # timeout = 2
        # begin = time.time()
        # while True:
        #
        #     try:
        #         client.send('USER')
        #     except:
        #         break
        #         # self.msg_box("Broken pipe", "Your socket pipe closed")
        #
        #     if time.time() - begin > timeout * 2 and all_recv["No data"] == "oh":
        #         self.msg_box("time out", "time out no data recieved")
        #         print "time out"
        #
        #     try:
        #         user_name = client.recvfrom(32)
        #         print user_name[0]
        #
        #         self.helloText.setText(user_name)
        #
        #         if user_name[0] == "oh":
        #             all_recv["No data"] = user_name[0]
        #             begin = time.time()
        #         else:
        #             # sleep for sometime to indicate a gap
        #             time.sleep(0.1)
        #
        #     except:
        #         pass
        # client.close()

    def check_(self,ip):
        try:
            socket.gethostbyaddr(ip)
            return True
        except socket.error:
            self.msg_box("Connection Refused", "The Address You Are Trying To Reach Is Currently Unavailable")
            return False


    def msg_box(self, title, data):
        w = QWidget()
        QMessageBox.information(w, title, data)



    def start_plot(self,T,P,A):
        plot_obj =  dynamic_plot()
        plot_obj2=  dynamic_plot()
        plot_obj3 = dynamic_plot()

        plot_obj.set_figure(self.AltPlot,self.canvas3)
        plot_obj2.set_figure(self.tempPlot,self.canvas1)
        plot_obj3.set_figure(self.PressPlot, self.canvas2)


        plot_obj.update_plot(self.t_counter,T)
        plot_obj2.update_plot(self.t_counter,P)
        plot_obj3.update_plot(self.t_counter,A)



class dynamic_plot(object):

    def __init__(self,):
        super(dynamic_plot, self).__init__()


    def set_figure(self,Figure,Canvas):
        self.figure = Figure
        self.canvas = Canvas

    def init_fig(self):
        self.xdata = []
        self.ydata = []
        self.lines,= self.figure.plot(self.xdata, self.ydata, 'o')   #load last plotted data
        self.figure.set_autoscaley_on(True)           # Autoscale on unknown axes or lims on known one/s
        self.figure.grid


    def on_running(self, xdata, ydata):
        # Update data (with the new _and_ the old points)
        self.lines.set_xdata(xdata)
        self.lines.set_ydata(ydata)
        # Need both of these in order to rescale
        self.figure.relim()
        self.figure.autoscale_view()
        self.canvas.draw()
        self.canvas.flush_events()


    def update_plot(self, x, y):
        self.init_fig()
        self.xdata.append(x)
        self.ydata.append(y)
        self.on_running(self.xdata, self.ydata)



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec_())
