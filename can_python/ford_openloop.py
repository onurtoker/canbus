# CAN bus send to MCU

from mykvaser import CanSender, CanReceiver, FifoWriter
import math
import queue
import time
from dataspeed import *

# Sender functions
func1 = lambda t: 180*math.cos(t/3)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    q1 = queue.Queue(100)

    fw = FifoWriter(func_list=[func1], fifo_list=[q1])
    fw.start()

    cs = CanSender(virtual  =False,
                   fid_list =[steering_command_fid],
                   func_list=[steering_command_enc],
                   fifo_list=[q1])
    cs.start()

    # app = QtWidgets.QApplication([])
    # rp = RtPlotter(fifo_list=[q1, q2], name_list=['Data1','Data2'], file_list=['data1.txt', 'data2.txt'])
    # rp.run(app)

    time.sleep(60)
    cs.stop()
