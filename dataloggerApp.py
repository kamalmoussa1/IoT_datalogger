'''
Data Logger V0.1 Demo  :: (GUI and Plotting)

Author: Kamal Moussa
Created 5 Nov 2016

'''


import sys
import socket
import time

import numpy as np


from PyQt4 import QtGui

import random
from PyQt4.uic import loadUiType      #to load window.ui
from PyQt4 import QtGui,QtCore

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

import matplotlib.pyplot as plt

begin = 0

class Demo(QtGui.QWidget):


    def __init__(self):
        super(Demo, self).__init__()

        self.initUI()

        self.connectButton.clicked.connect(self.client_send_message)



    # def start_server(self):
        # ip_address


    def initUI(self):

        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(16)

        font2 = QtGui.QFont()
        font2.setPointSize(18)


        self.lineEdit= QtGui.QLineEdit()
        self.connectButton= QtGui.QPushButton("Connect")
        self.helloText =QtGui.QTextEdit()

        self.lineEdit.setMaximumWidth(250)
        self.lineEdit.setMinimumWidth(150)
        self.lineEdit.setFont(font2)
        self.lineEdit.setPlaceholderText("What IP, please?")


        self.connectButton.setMaximumWidth(350)
        self.connectButton.setMinimumWidth(150)
        self.connectButton.setFont(font)

        self.helloText.setMaximumWidth(500)
        self.helloText.setMinimumWidth(300)
        self.helloText.setMaximumHeight(100)
        self.helloText.setMinimumHeight(50)
        self.helloText.setFont(font)


        # self.Tlabel = QtGui.QLabel("Temperature")
        # self.Plabel = QtGui.QLabel("Pressure")
        # self.Alabel = QtGui.QLabel("Altitude")


        hEbox =QtGui.QHBoxLayout()
        hEbox.addStretch()
        hEbox.addWidget(self.lineEdit)
        hEbox.addStretch()
        hEbox.setContentsMargins(0,100,0,0)

        hBbox = QtGui.QHBoxLayout()
        hBbox.addStretch()
        hBbox.addWidget(self.connectButton)
        hBbox.addStretch()
        hBbox.setContentsMargins(0, 15, 0, 0)

        hTbox=QtGui.QHBoxLayout()
        hTbox.addStretch()
        hTbox.addWidget(self.helloText)
        hTbox.addStretch()
        hTbox.setContentsMargins(0,20,0,70)

        self.plot_config()

        #-------Graphs box-----------#
        hWbox = QtGui.QHBoxLayout()
        hWbox.addWidget(self.canvas1)
        hWbox.addWidget(self.canvas2)
        hWbox.addWidget(self.canvas3)
        hWbox.setContentsMargins(20,0,20,50)


        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hEbox)
        vbox.addLayout(hBbox)
        vbox.addLayout(hTbox)
        vbox.addLayout(hWbox)


        self.setLayout(vbox)
        self.setGeometry(350, 200, 1200, 800)
        self.setMinimumSize(700, 700)
        self.setWindowTitle('Data Logger V 0.1')

    def plot_config(self):
        self.fig1 = Figure()
        self.fig2 = Figure()
        self.fig3 = Figure()

        self.canvas1 = FigureCanvas(self.fig1)
        self.canvas2 = FigureCanvas(self.fig2)
        self.canvas3 = FigureCanvas(self.fig3)



        self.tempPlot = self.fig1.add_subplot(111)
        self.PressPlot = self.fig2.add_subplot(111)
        self.AltPlot = self.fig3.add_subplot(111)

        self.tempPlot.set_title('Temperature Log')
        self.tempPlot.set_xlabel('t (s)')
        self.tempPlot.set_ylabel('T (C)')

        self.PressPlot.set_title('Pressure Log')
        self.PressPlot.set_xlabel('t (s)')
        self.PressPlot.set_ylabel('P (hPa)')

        self.AltPlot.set_title('Altitude Log')
        self.AltPlot.set_xlabel('t (s)')
        self.AltPlot.set_ylabel('A (m)')


    def _get(self):
        return tmp

    def client_send_message(self):

        #----- Autour: Ahmed Atallah-------#

        # self.connectButton.setCursor(Qt.WaitCursor)
        # time.sleep(1)    #wait 1 second
        # self.connectButton.setCursor(Qt.ArrowCursor)

        # ip_address = self.lineEdit.text()
        # ip_address = '192.168.43.71'
        ip_address = '192.168.1.104'
        print (ip_address)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # msg_box("", "Socket Created")
        try:
            client.connect((ip_address, 80))

        except Exception, e:
            self.msg_box("Connection Refused", "The Address You Are Trying To Reach Is Currently Unavailable")

        timeout = 2
        all_data = {"User": "", "Temp": "", "Press": "", "Altit": ""}
        begin = time.time()
        if all_data:
            print "Data is being recieved ...."
        while True:
            try:
                client.send('GET')
            except:
                # msg_box("Broken pipe", "Your socket pipe closed")
                break

            # if you got no data at all, wait a little longer, twice the timeout
            if time.time() - begin > timeout*2:
                self.msg_box("time out", "time out no data recieved")
                break
            # print time.time()

            # recv something
            try:

                i = -1
                # senss = client.recvfrom(16)
                sensors_out = client.recvfrom(32)
                print sensors_out[0]



                sensor_D = sensors_out[0].split(',')
                # senss_D = senss[0].split(',')
                # all_D = sensor_D + senss_D
                # all_D = sensor_D
                if sensors_out[0] != "":
                    i += 1
                    # self._get(self,sensor_D[4 * i])
                    all_data['User'] += (sensor_D[4 * i] + ',')
                    all_data['Temp'] += (sensor_D[4 * i + 1] + ',')
                    all_data['Press'] += (sensor_D[4 * i + 2] + ',')
                    all_data['Altit'] += (sensor_D[4 * i + 3] + ',')

                    # change the beginning time for measurement
                    begin = time.time()
                else:
                    # sleep for sometime to indicate a gap
                    time.sleep(0.1)


            except:
                pass


        # pressAfter = all_data["Press"].split(',')
        # print sensors_out[0]

        client.close()





    def plot_signal(self):
        Fs = 8000
        f = 5
        sample = 8000
        x = np.arange(sample)
        y = np.sin(2 * np.pi * f * x / Fs)
        self.tempPlot.plot(x,y)
        self.tempPlot.hold(True)
        self.canvas1.draw()


    def msg_box(self, title, data):
        w = QWidget()
        QMessageBox.information(w, title, data)

class Plot(object):

    def __init__(self):
        super(Plot, self).__init__()


    def test(self):
        print 'H'



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    demo = Demo()
    demo.show()
    demo.plot_signal()
    # demo.client_send_message()
    sys.exit(app.exec_())
