# Ford CAN closed loop

from PyQt5 import QtWidgets, QtCore, QtGui
from myplotter import RtPlotter
from mykvaser import CanSender, CanReceiver
import queue
from dataspeed import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    q1 = queue.Queue(100)
    q2 = queue.Queue(100)
    q3 = queue.Queue(100)
    q4 = queue.Queue(100)

    cr = CanReceiver(virtual    =False,
                     fid_list   =[wheel_report_fid, breakPC_report_fid],
                     func_list  =[wheel_report_dec, breakPC_report_dec],
                     fifo_list  =[q1, q2])
    cr.start()

    app = QtWidgets.QApplication([])
    rp = RtPlotter(fifo_list    =[q1, q2],
                   name_list    =[wheel_report_legend, breakPC_report_legend],
                   file_list    =[wheel_report_file,   breakPC_report_file])

    rp.run(app)

    cr.stop()
