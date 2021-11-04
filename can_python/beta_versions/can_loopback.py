# CAN loopback

from canlib import canlib, Frame
import threading
import time


def can_send_thread():

    ch0 = canlib.openChannel(
        channel=0,
        flags=canlib.Open.ACCEPT_VIRTUAL,
        bitrate= canlib.canBITRATE_250K,
    )
    # Set the CAN bus driver type to NORMAL.
    ch0.setBusOutputControl(canlib.Driver.NORMAL)
    # Activate the CAN chip.
    ch0.busOn()

    for i in range(100):
        frame = Frame(id_=0x124, data=b'HELLO!  ', dlc=8)
        ch0.write(frame)
        str = 'MSG__' + '%03d' % (i,)
        my_data = bytes(str, 'utf-8')
        frame = Frame(id_=0x123, data=my_data, dlc=8)
        # print(frame)
        ch0.write(frame)
        time.sleep(0.01)

        # Wait until the message is sent or at most 100 ms.
        try:
            ch0.writeSync(timeout=100)
        except canlib.canError as ex:
            print('CAN write:', ex)
            break

    # Inactivate the CAN chip.
    ch0.busOff()
    # Close the channel.
    ch0.close()


def can_recv_thread():

    ch1 = canlib.openChannel(
        channel=1,
        flags=canlib.Open.ACCEPT_VIRTUAL,
        bitrate= canlib.canBITRATE_250K,
    )
    # Set accept filter
    ch1.canAccept(0x7ff, canlib.AcceptFilterFlag.SET_MASK_STD)
    ch1.canAccept(0x123, canlib.AcceptFilterFlag.SET_CODE_STD)
    # Set the CAN bus driver type to NORMAL.
    ch1.setBusOutputControl(canlib.Driver.NORMAL)
    # Activate the CAN chip.
    ch1.busOn()

    counter = 0
    while True:
        try:
            frame = ch1.read(timeout=1000)
            counter += 1
            print('%06d' % (counter,),  ":", frame.data.decode('utf-8'), '@', frame.timestamp, 'ms')
        except canlib.canNoMsg as ex:
            print('CAN read timeout')
            break
        except canlib.canError as ex:
            print('CAN read:', ex)
            break

    # Inactivate the CAN chip.
    ch1.busOff()
    # Close the channel.
    ch1.close()


def main():

    thr_send = threading.Thread(target=can_send_thread)
    thr_recv = threading.Thread(target=can_recv_thread)

    thr_send.start()
    thr_recv.start()

    thr_send.join()


if __name__ == "__main__":
    main()