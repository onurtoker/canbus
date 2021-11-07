# Ford CAN bus plotter

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
                     fid_list   =[throttle_report_fid, break_report_fid, speed_report_fid],
                     func_list  =[throttle_report_dec, break_report_dec, speed_report_dec],
                     fifo_list  =[q1, q2, q3])
    cr.start()

    app = QtWidgets.QApplication([])
    rp = RtPlotter(fifo_list    =[q1, q2, q3],
                   name_list    =[throttle_report_legend, break_report_legend, speed_report_legend],
                   file_list    =[throttle_report_file,   break_report_file,   speed_report_file])

    rp.run(app)

    cr.stop()
