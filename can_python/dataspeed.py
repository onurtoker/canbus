import struct

# STEERING ANGLE REPORT
steering_report_legend = 'SteeringR'
steering_report_file = 'SteeringR.txt'
steering_report_fid = 0x065
steering_report_dec = lambda x: 0.1*struct.unpack('h', x[0:2])[0]

# STEERING ANGLE COMMAND
steering_command_legend = 'SteeringC'
steering_command_file = 'SteeringC.txt'
steering_command_fid = 0x064
def steering_command_enc(a):
    if a < -400:
        a = -400
    elif a > 400:
        a = 400
    bm=bytearray(8)
    iv = round(10*a)
    bx=struct.pack('h', iv)
    bm[0]=bx[0]
    bm[1]=bx[1]
    bm[2]=0x03 # use angle, CLEAR=1, EN=1
    bm[3]=0x10 # max speed 64 degrees/sec
    bm[4]=bm[5]=bm[6]=bm[7]=0
    return bm


# THROTTLE REPORT
throttle_report_legend = 'ThrottleR'
throttle_report_file = 'ThrottleR.txt'
throttle_report_fid = 0x063
throttle_report_dec = lambda x: struct.unpack('H', x[0:2])[0] / 655.35

# THROTTLE COMMAND
throttle_command_legend = 'ThrottleC'
throttle_command_file = 'ThrottleC.txt'
throttle_command_fid = 0x062
def throttle_command_enc(a):
    if a < 0:
        a = 0
    elif a > 100:
        a = 100
    bm=bytearray(8)
    iv = round(655.35*a)
    bx=struct.pack('H', iv)
    bm[0]=bx[0]
    bm[1]=bx[1]
    bm[2]=0x20 # use percent throttle
    bm[3]=0x03 # CLEAR=1, EN=1
    bm[4]=bm[5]=bm[6]=bm[7]=0
    return bm


# BREAK REPORT
break_report_legend = 'BreakR'
break_report_file = 'BreakR.txt'
break_report_fid = 0x061
break_report_dec = lambda x: struct.unpack('H', x[0:2])[0] / 655.35

# BREAK_PC REPORT
breakPC_report_legend = 'BreakPC'
breakPC_report_file = 'BreakPC.txt'
breakPC_report_fid = 0x061
breakPC_report_dec = lambda x: struct.unpack('H', x[2:4])[0] / 655.35

# BREAK COMMAND
break_command_legend = 'BreakC'
break_command_file = 'BreakC.txt'
break_command_fid = 0x060
def break_command_enc(a):
    if a < 0:
        a = 0
    if a > 100:
        a = 100
    bm=bytearray(8)
    iv = round(655.35*a)
    bx=struct.pack('H', iv)
    bm[0]=bx[0]
    bm[1]=bx[1]
    bm[2]=0x20 # use percent throttle
    bm[3]=0x03 # CLEAR=1, EN=1
    bm[4]=bm[5]=bm[6]=bm[7]=0
    return bm


# SPEED REPORT
speed_report_legend = 'Speed'
speed_report_file = 'Speed.txt'
speed_report_fid = 0x065
speed_report_dec = lambda x: 0.01*struct.unpack('H', x[4:6])[0]

# RPM REPORT
rpm_report_legend = 'RPM'
rpm_report_file = 'RPM.txt'
rpm_report_fid = 0x075
rpm_report_dec = lambda x: 0.25*struct.unpack('H', x[0:2])[0]

# WHEEL SPEED REPORT
wheel_report_legend = 'Wheel'
wheel_report_file = 'Wheel.txt'
wheel_report_fid = 0x06A
wheel_report_dec = lambda x: 0.01*( struct.unpack('h', x[0:2])[0] +
                                    struct.unpack('h', x[2:4])[0] +
                                    struct.unpack('h', x[4:6])[0] +
                                    struct.unpack('h', x[6:8])[0]) / 4