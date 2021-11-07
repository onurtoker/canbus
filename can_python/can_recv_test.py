# CAN recv test

from canlib import canlib, Frame
import threading
import time


def can_recv_thread():

    ch1 = canlib.openChannel(
        channel=0,
        flags=canlib.Open.EXCLUSIVE,
        bitrate= canlib.canBITRATE_500K,
    )

    # Set accept filter
    # ch1.canAccept(0x7ff, canlib.AcceptFilterFlag.SET_MASK_STD)
    # ch1.canAccept(0x123, canlib.AcceptFilterFlag.SET_CODE_STD)

    # Set the CAN bus driver type to NORMAL.
    ch1.setBusOutputControl(canlib.Driver.NORMAL)

    # Activate the CAN chip.
    ch1.busOn()

    counter = 0
    while True:
        try:
            frame = ch1.read(timeout=5000)
            counter += 1
            data_str = ''.join('{:02x} '.format(x) for x in frame.data)
            print('%06d' % counter, '0x%04x' % frame.id,  ":", data_str, '@', frame.timestamp, 'ms')
        except canlib.canNoMsg as ex:
            print('CAN read timeout')
            break
        except canlib.canError as ex:
            print('CAN read', ex)
            break

    # Inactivate the CAN chip.
    ch1.busOff()
    # Close the channel.
    ch1.close()


def main():

    thr_recv = threading.Thread(target=can_recv_thread, daemon=True)

    thr_recv.start()
    thr_recv.join()


if __name__ == "__main__":
    main()