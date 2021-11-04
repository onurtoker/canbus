# my Kvaser tools

from canlib import canlib, Frame
import threading
import time

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
            for (fid, (func, enc), fifo) in zip(self.fid_list, self.func_list, self.fifo_list):
                t = time.time() - self.origin
                y = func(t)
                if not(fifo is None):
                    fifo.put((t,y), timeout=100)
                frame = Frame(id_=fid, data=enc(y), dlc=8)
                # print(frame)

                # Wait until the message is sent or at most 100 ms.
                try:
                    self.ch.write(frame)
                    time.sleep(0.02)  # rate is fixed, not configurable
                    self.ch.writeSync(timeout=1000)      # timeout is fixed, not configurable
                except canlib.canError as ex:
                    print('CAN write:', ex)
                    pass
                    # return

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
                    ix = self.fid_list.index(frame.id)
                    tx = frame.timestamp / 1000
                    dx = self.func_list[ix](frame.data)
                    self.fifo_list[ix].put((tx, dx), timeout=100)
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
