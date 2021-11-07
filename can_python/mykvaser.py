# my Kvaser tools

from canlib import canlib, Frame
import threading
import time
import numpy as np

class CanSender:

    def __init__(self, fid_list, func_list, fifo_list, virtual=True):
        self.virtual = virtual
        self.ch = None
        self.fid_list = fid_list
        self.func_list = func_list
        self.fifo_list = fifo_list
        self.origin = time.time()

    def __can_open(self):
        if self.virtual:
            self.ch = canlib.openChannel(channel=0, flags=canlib.Open.ACCEPT_VIRTUAL, bitrate= canlib.canBITRATE_500K)
        else:
            self.ch = canlib.openChannel(channel=0, flags=canlib.Open.EXCLUSIVE, bitrate=canlib.canBITRATE_500K)

        # Set the CAN bus driver type to NORMAL.
        self.ch.setBusOutputControl(canlib.Driver.NORMAL)
        # Activate the CAN chip.
        self.ch.busOn()

    def __main_loop(self):
        while True:
            for (fid, enc, fifo) in zip(self.fid_list, self.func_list, self.fifo_list):

                try:
                    (t,y) = fifo.get(timeout=100e-3)
                    frame = Frame(id_=fid, data=enc(y), dlc=8)
                except Exception as ex:
                    continue

                frame = Frame(id_=fid, data=enc(y), dlc=8)
                # print(frame)

                # Wait until the message is sent or at most 1000 ms.
                try:
                    self.ch.write(frame)
                    self.ch.writeSync(timeout=1000)      # timeout is fixed, not configurable
                except canlib.canError as ex:
                    print('CAN write:', ex)
                    pass
                    # return

                time.sleep(0.02)  # rate is fixed, not configurable


    def __can_close(self):
        # Inactivate the CAN chip.
        self.ch.busOff()
        # Close the channel.
        self.ch.close()

    def start(self):
        self.__can_open()
        thr_send = threading.Thread(target=self.__main_loop, daemon=True)
        thr_send.start()

    def stop(self):
        self.__can_close()


class CanReceiver:

    def __init__(self, fid_list, func_list, fifo_list, virtual=True):
        self.virtual = virtual
        self.ch = None
        self.fid_list = fid_list
        self.func_list = func_list
        self.fifo_list = fifo_list
        self.origin = time.time()

    def __can_open(self):
        if self.virtual:
            self.ch = canlib.openChannel(channel=1, flags=canlib.Open.ACCEPT_VIRTUAL, bitrate= canlib.canBITRATE_500K)
        else:
            self.ch = canlib.openChannel(channel=0, flags=canlib.Open.EXCLUSIVE, bitrate=canlib.canBITRATE_500K)

        # # Set accept filter
        # self.ch.canAccept(0x7ff, canlib.AcceptFilterFlag.SET_MASK_STD)
        # self.ch.canAccept(0x123, canlib.AcceptFilterFlag.SET_CODE_STD)

        # Set the CAN bus driver type to NORMAL.
        self.ch.setBusOutputControl(canlib.Driver.NORMAL)
        # Activate the CAN chip.
        self.ch.busOn()

    def __main_loop(self):
        while True:
            try:
                frame = self.ch.read(timeout=1000)  # timeout is fixed, not configurable
                # print(hex(frame.id), ':', frame.data, '@', frame.timestamp, 'ms')
                try:
                    # ix = self.fid_list.index(frame.id)
                    indices = [ix for (ix, fid) in enumerate(self.fid_list) if fid == frame.id]
                    for ix in indices:
                        tx = frame.timestamp / 1000
                        dx = self.func_list[ix](frame.data)
                        # print(frame)
                        self.fifo_list[ix].put((tx, dx), timeout=100e-3)
                except ValueError as ex:
                    pass

            except canlib.canNoMsg as ex:
                print('CAN read timeout')
                pass
                # return
            except canlib.canError as ex:
                print('CAN read:', ex)
                return

    def __can_close(self):
        # Inactivate the CAN chip.
        self.ch.busOff()
        # Close the channel.
        self.ch.close()

    def start(self):
        self.__can_open()
        thr_recv = threading.Thread(target=self.__main_loop, daemon=True)
        thr_recv.start()

    def stop(self):
        self.__can_close()


class FifoWriter:

    def __init__(self, func_list, fifo_list):
        self.func_list = func_list
        self.fifo_list = fifo_list
        self.origin = time.time()

    def __main_loop(self):
        while True:
            for (func, fifo) in zip(self.func_list, self.fifo_list):
                t = time.time() - self.origin
                y = func(t)
                try:
                    fifo.put((t, y), timeout=100e-3)
                except Exception as ex:
                    print('FifoWriter', ex)
                    return
                time.sleep(0.02)  # rate is fixed, not configurable

    def start(self):
        thr = threading.Thread(target=self.__main_loop, daemon=True)
        thr.start()

class TeeBlock:

    def __init__(self, qi, qo1, qo2):
        self.qi = qi
        self.qo1 = qo1
        self.qo2 = qo2

    def __main_loop(self):
        while True:
            e = self.qi.get()
            self.qo1.put(e)
            self.qo2.put(e)

    def start(self):
        thr = threading.Thread(target=self.__main_loop, daemon=True)
        thr.start()


class NullSink:

    def __init__(self, qi):
        self.qi = qi

    def __main_loop(self):
        while True:
            print(self.qi.get())

    def start(self):
        thr = threading.Thread(target=self.__main_loop, daemon=True)
        thr.start()


class Controller:

    def __init__(self, qi, qo, func):
        self.qi = qi
        self.qo = qo
        self.func = func

    def __main_loop(self):
        while True:
            if not self.qi.empty():
                t, x = self.qi.get()
                t, y = self.func(t, x)
                self.qo.put((t, y), timeout=100e-3)

    def start(self):
        thr = threading.Thread(target=self.__main_loop, daemon=True)
        thr.start()


class FileWriter:

    def __init__(self, qi, fname):
        self.qi = qi
        self.fid = open(fname, 'w')

    def __main_loop(self):
        while True:
            t, x = self.qi.get()
            print('%8.3f' % t)
            self.fid.write('%8.3f, %8.3f \n' % (t, x))

    def start(self):
        thr = threading.Thread(target=self.__main_loop, daemon=True)
        thr.start()

    def stop(self):
        self.fid.flush()
        self.fid.close()