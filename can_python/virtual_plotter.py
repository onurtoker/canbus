# virtual CAN bus plotter

from PyQt5 import QtWidgets, QtCore, QtGui
from myplotter import RtPlotter
from mykvaser import CanSender, CanReceiver
import math
import queue

# Sender functions
func1 = lambda x: math.cos(x)
enc1 = lambda x: bytes('%8.3f' % x, 'utf-8')
func2 = lambda x: math.sin(x)
enc2 = lambda x: bytes('%8.3f' % x, 'utf-8')

# Receiver functions
dec1 = lambda x: float(x.decode('utf-8'))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    q1 = queue.Queue(100)
    q2 = queue.Queue(100)

    # cs = CanSender(virtual=True, fid_list=[0x111, 0x222], func_list=[(func1, enc1), (func2, enc2)], fifo_list=[q1, q2])
    # cs.start()

    cs = CanSender(virtual=True, fid_list=[0x111, 0x222], func_list=[(func1, enc1), (func2, enc2)], fifo_list=[None, None])
    cs.start()
    cr = CanReceiver(virtual=True, fid_list=[0x111, 0x222], func_list=[dec1, dec1], fifo_list=[q1, q2])
    cr.start()

    app = QtWidgets.QApplication([])
    rp = RtPlotter(fifo_list=[q1, q2], name_list=['Data1','Data2'], file_list=['data1.txt', 'data2.txt'])
    rp.run(app)

    cs.stop()
    cr.stop()
