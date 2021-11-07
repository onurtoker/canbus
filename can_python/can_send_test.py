# CAN send test

from canlib import canlib, Frame
import threading
import time


def can_send_thread():

    ch1 = canlib.openChannel(
        channel=0,
        flags=canlib.Open.EXCLUSIVE,
        bitrate= canlib.canBITRATE_500K,
    )

    # Set the CAN bus driver type to NORMAL.
    ch1.setBusOutputControl(canlib.Driver.NORMAL)

    # Activate the CAN chip.
    ch1.busOn()

    counter = 0
    while True:
        frame = Frame(id_=0x111, data=bytearray(8*[0]), dlc=8)
        for i in range(7):
            frame.data[i] = i + 1
        frame.data[7] = counter % 256
        counter += 1

        ch1.write(frame)
        print(frame)
        time.sleep(0.1)

        # Wait until the message is sent or at most 1000 ms.
        try:
            ch1.writeSync(timeout=1000)
        except canlib.canError as ex:
            print('CAN write', ex)
            break

    # Inactivate the CAN chip.
    ch1.busOff()
    # Close the channel.
    ch1.close()


def main():

    thr_send = threading.Thread(target=can_send_thread, daemon=True)
    thr_send.start()
    thr_send.join()


if __name__ == "__main__":
    main()