# my real-time plotter tools

from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
import threading
import time
import numpy as np


class RtPlotter(QtWidgets.QMainWindow):

    def __init__(self, fifo_list, name_list, file_list, *args, **kwargs):
        super(RtPlotter, self).__init__(*args, **kwargs)

        self.fifo_list = fifo_list
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.addLegend()
        self.file_list = file_list
        # self.graphWidget.setBackground('w')

        self.curves = len(fifo_list) * [None]
        self.fids = len(fifo_list) * [None]
        for (k, fifo) in enumerate(fifo_list):
            xvals = np.zeros(1000)  # 100 time points
            yvals = np.zeros(1000)  # 100 time points
            curve = self.graphWidget.plot(xvals, yvals, pen=pg.intColor(k), name=name_list[k],
                                          symbol='s', symbolBrush=pg.intColor(k), symbolPen='w')
            self.curves[k] = [xvals, yvals, curve]

            if not(self.file_list[k] is None):
                self.fids[k] = open(file_list[k], 'w')

        # Timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.__update_plot_data)
        self.timer.start()

    def __update_plot_data(self):
        for (k,(xvals, yvals, curve)) in enumerate(self.curves):
            sz = self.fifo_list[k].qsize()
            if (sz < 5): continue
            xn = np.zeros(sz)
            yn = np.zeros(sz)
            for i in range(sz):
                (xn[i], yn[i]) = self.fifo_list[k].get(timeout=100e-3)
                if not(self.file_list[k] is None):
                    self.fids[k].write('%8.3f, %8.3f \n' % (xn[i], yn[i]))

            xvals = self.curves[k][0]
            self.curves[k][0] = xvals = np.append(xvals[sz:], xn)
            yvals = self.curves[k][1]
            self.curves[k][1] = yvals = np.append(yvals[sz:], yn)
            curve = self.curves[k][2]
            curve.setData(xvals, yvals)

            # except Exception as ex:
            #     print('RtPlotter', ex)

    def run(self, app):
        self.setWindowTitle('GraphWindow')
        self.show()
        app.exec_()

        for fid in self.fids:
            if not(fid is None):
                fid.close()