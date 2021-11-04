from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
from canlib import canlib, Frame
import threading
import time
from math import *
import queue
import sys

ch0 = canlib.openChannel(
    channel=0,
    flags=canlib.Open.ACCEPT_VIRTUAL,
    bitrate=canlib.canBITRATE_250K,
)

ch1 = canlib.openChannel(
    channel=1,
    flags=canlib.Open.ACCEPT_VIRTUAL,
    bitrate=canlib.canBITRATE_250K,
)

class GraphWindow(QtWidgets.QMainWindow):

    def __init__(self, data_fifo, data_fifo2, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)

        self.fifo = data_fifo
        self.fifo2 = data_fifo2

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.x = [0 for _ in range(500)]  # 100 time points
        self.y = [0 for _ in range(500)]  # 100 data points
        self.x2 = [0 for _ in range(500)]  # 100 time points
        self.y2 = [0 for _ in range(500)]  # 100 data points

        self.graphWidget.showGrid(x=True, y=True)
        #self.graphWidget.setBackground('w')
        pen = pg.mkPen(QtGui.QColor('yellow'))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        pen = pg.mkPen(QtGui.QColor('red'))
        self.data_line2 =  self.graphWidget.plot(self.x2, self.y2, pen=pen)

        # Timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        sz = self.fifo.qsize()
        for k in range(sz):
            try:
                (xn, yn) = self.fifo.get(timeout=0.01)
                self.x = self.x[1:]  # Remove the first y element.
                self.x.append(xn)  # Add a new value 1 higher than the last.
                self.y = self.y[1:]  # Remove the first
                self.y.append(yn)  # Add a new value 1 higher than the last.
            except Exception as ex:
                print(ex)
        self.data_line.setData(self.x, self.y)  # Update the data.

        sz = self.fifo2.qsize()
        for k in range(sz):
            try:
                (xn, yn) = self.fifo2.get(timeout=0.01)
                self.x2 = self.x2[1:]  # Remove the first y element.
                self.x2.append(xn)  # Add a new value 1 higher than the last.
                self.y2 = self.y2[1:]  # Remove the first
                self.y2.append(yn)  # Add a new value 1 higher than the last.
            except Exception as ex:
                print(ex)
        self.data_line2.setData(self.x2, self.y2)  # Update the data.


def graph_thread(q, q2):
    app = QtWidgets.QApplication([])
    w = GraphWindow(q, q2)
    w.setWindowTitle('GraphWindow')
    w.show()
    app.exec_()


def can_send_thread():

    # ch0 = canlib.openChannel(
    #     channel=0,
    #     flags=canlib.Open.ACCEPT_VIRTUAL,
    #     bitrate= canlib.canBITRATE_250K,
    # )

    # Set the CAN bus driver type to NORMAL.
    ch0.setBusOutputControl(canlib.Driver.NORMAL)
    # Activate the CAN chip.
    ch0.busOn()

    for i in range(1000):
        frame = Frame(id_=0x200, data=b'HELLO!  ', dlc=8)
        ch0.write(frame)

        str = '%8.3f' % (cos(0.2*i),)
        my_data = bytes(str, 'utf-8')
        frame = Frame(id_=0x121, data=my_data, dlc=8)
        ch0.write(frame)

        str = '%8.3f' % (sin(0.2*i),)
        my_data = bytes(str, 'utf-8')
        frame = Frame(id_=0x122, data=my_data, dlc=8)
        ch0.write(frame)

        time.sleep(0.05)

        # Wait until the message is sent or at most 500 ms.
        try:
            ch0.writeSync(timeout=100)
        except canlib.canError as ex:
            # print('CAN write: ', ex)
            break

    # # Inactivate the CAN chip.
    # ch0.busOff()
    # # Close the channel.
    # ch0.close()


def can_recv_thread(q, q2):

    # ch1 = canlib.openChannel(
    #     channel=1,
    #     flags=canlib.Open.ACCEPT_VIRTUAL,
    #     bitrate= canlib.canBITRATE_250K,
    # )

    # # Set accept filter
    # ch1.canAccept(0x7ff, canlib.AcceptFilterFlag.SET_MASK_STD)
    # ch1.canAccept(0x123, canlib.AcceptFilterFlag.SET_CODE_STD)

    # Set the CAN bus driver type to NORMAL.
    ch1.setBusOutputControl(canlib.Driver.NORMAL)
    # Activate the CAN chip.
    ch1.busOn()

    counter = 0
    while True:
        try:
            frame = ch1.read(timeout=1000)
            counter += 1
            # print('%06d' % (counter,),  ":", frame.data.decode('utf-8'), '@', frame.timestamp, 'ms')
            if frame.id == 0x121:
                tx = frame.timestamp
                dx = float(frame.data.decode('utf-8'))
                q.put((tx, dx), timeout=1000)
            elif frame.id == 0x122:
                tx = frame.timestamp
                dx = float(frame.data.decode('utf-8'))
                q2.put((tx, dx), timeout=1000)
        except canlib.canNoMsg as ex:
            print('CAN read timeout')
            break
        except canlib.canError as ex:
            # print('CAN read:', ex)
            break

    # # Inactivate the CAN chip.
    # ch1.busOff()
    # # Close the channel.
    # ch1.close()


def main():

    q = queue.Queue(100)
    q2 = queue.Queue(100)

    thr_send = threading.Thread(target=can_send_thread)
    thr_recv = threading.Thread(target=can_recv_thread, args=(q,q2,))
    thr_send.start()
    thr_recv.start()

    # g_thr = threading.Thread(target=graph_thread, args=(q,))
    # g_thr.daemon = True
    # g_thr.start()

    # Main thread
    graph_thread(q, q2)

    ch0.close()
    ch1.close()


if __name__ == "__main__":
    main()
