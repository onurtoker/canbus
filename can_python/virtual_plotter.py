# virtual CAN bus plotter

from PyQt5 import QtWidgets, QtCore, QtGui
from myplotter import RtPlotter
from mykvaser import CanSender, CanReceiver, FifoWriter, TeeBlock, NullSink, Controller, FileWriter
import math
import queue
import time

# Sender functions
func1 = lambda x: math.cos(x)
enc1 = lambda x: bytes('%8.3f' % x, 'utf-8')
func2 = lambda x: math.sin(x)
enc2 = lambda x: bytes('%8.3f' % x, 'utf-8')

# Receiver functions
dec1 = lambda x: float(x.decode('utf-8'))

# Controller functions
def fc(tL, xL):
    return tL, 2*xL

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    q1 = queue.Queue(100)
    q2 = queue.Queue(100)
    q3 = queue.Queue(100)
    q4 = queue.Queue(100)
    q5 = queue.Queue(100)
    q1a = queue.Queue(100)
    q1b = queue.Queue(100)

    fw = FifoWriter(func_list=[func1], fifo_list=[q1])
    fw.start()

    # tb = TeeBlock(q1, q1a, q1b)
    # tb.start()

    ct = Controller(q1, q2, fc)
    ct.start()

    fx = FileWriter(q2, 'Data.txt')
    fx.start()

    time.sleep(100)

    fx.stop()

    # cs = CanSender(virtual=True, fid_list=[0x111, 0x222], func_list=[enc1, enc2], fifo_list=[q1, q2])
    # cs.start()
    # cr = CanReceiver(virtual=True, fid_list=[0x111, 0x222], func_list=[dec1, dec1], fifo_list=[q3, q4])
    # cr.start()

    # app = QtWidgets.QApplication([])
    # rp = RtPlotter(fifo_list=[q1], name_list=['-','-'], file_list=[None, None])
    # rp.run(app)

    # cs.stop()
    # cr.stop()
