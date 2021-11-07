# CAN bus send to MCU

from mykvaser import CanSender, CanReceiver
import math
import queue
import time

# Sender functions
func1 = lambda x: math.cos(x)
enc1 = lambda x: bytes('%8.3f' % x, 'utf-8')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    q1 = queue.Queue(100)

    cs = CanSender(virtual=False, fid_list=[0x111], func_list=[(func1, enc1)], fifo_list=[None])
    cs.start()

    time.sleep(60)
    cs.stop()
