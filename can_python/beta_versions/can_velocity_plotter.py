from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
from canlib import canlib, Frame
import threading
import time
from math import *
import queue
import sys

class GraphWindow(QtWidgets.QMainWindow):

    def __init__(self, data_fifo, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)

        self.fifo = data_fifo
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.x = [0 for _ in range(2500)]  # 100 time points
        self.y = [0 for _ in range(2500)]  # 100 data points
        self.graphWidget.showGrid(x=True, y=True)
        pen = pg.mkPen(QtGui.QColor('yellow'))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)

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


def graph_thread(q):
    app = QtWidgets.QApplication([])
    w = GraphWindow(q)
    w.setWindowTitle('GraphWindow')
    w.show()
    app.exec_()


def can_recv_thread(q):

    ch1 = canlib.openChannel(
        channel=0,
        flags=canlib.Open.EXCLUSIVE,
        bitrate= canlib.canBITRATE_500K,
    )
    # Set accept filter
    ch1.canAccept(0x7ff, canlib.AcceptFilterFlag.SET_MASK_STD)
    ch1.canAccept(0x06a, canlib.AcceptFilterFlag.SET_CODE_STD)
    # Set the CAN bus driver type to NORMAL.
    ch1.setBusOutputControl(canlib.Driver.NORMAL)
    # Activate the CAN chip.
    ch1.busOn()

    counter = 0
    while True:
        try:
            frame = ch1.read(timeout=1000)
            counter += 1
            data_str = ''.join('{:02x}'.format(x) for x in frame.data)
            # print('%06d' % (counter,),  ":", data_str, '@', frame.timestamp, 'ms')
            tx = frame.timestamp / 1000
            dx = 256 * float(frame.data[1]) + float(frame.data[0])
            q.put((tx, dx))
        except canlib.canNoMsg as ex:
            print('CAN read timeout')
            break
        except canlib.canError as ex:
            print('CAN read', ex)
            break

    # Inactivate the CAN chip.
    ch1.busOff()
    # Close the channel.
    ch1.close()


def main():

    q = queue.Queue(500)

    recv_thr = threading.Thread(target=can_recv_thread, args=(q,), daemon=True)
    recv_thr.start()

    # g_thr = threading.Thread(target=graph_thread, args=(q,))
    # g_thr.start()

    # Main thread
    graph_thread(q)


if __name__ == "__main__":
    main()
