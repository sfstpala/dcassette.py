#!/usr/bin/env python3
'''
    A 1 kBd Modem in python

    Note that the functions expect a unicode string.

'''

import wave

def write_wave(filename, transmission):
    data, transmission = [], "\x02" + transmission + "\x04"
    ONE = (bytes(b"\x00" * 16) + bytes(b"\xFF" * 16)) * 16
    ZERO = (bytes(b"\x00" * 8) + bytes(b"\xFF" * 8)) * 32
    for i in transmission:
        for j in bin(ord(i))[2:].rjust(16, "0"):
            data.append(ONE if j == "1" else ZERO)
    w = wave.open(filename, "w")
    w.setframerate(16000)
    w.setnchannels(1)
    w.setsampwidth(1)
    data = b''.join(data)
    w.writeframes(data)
    w.close()

def read_wave(filename):
    result, transmission = [], ""
    w = wave.open(filename, "r")
    sot = False
    min_, max_ = 0, 0
    while w.tell() < w.getnframes():
        tally = 0
        last = False
        for i in range(512):
            try:
                frame = w.readframes(1)[0] > (0xFF // 2)
            except IndexError:
                break
            if frame != last:
                tally += 1
            last = frame
        print(tally / 2 /16)
    
        if tally / 2 / 16 >= 1.8:
            result.append(0)
        else:
            result.append(1)
    w.close()
    return result
    if "\x02" in transmission:
        transmission = transmission.split("\x02")[1]
        if "\x04" in transmission:
            transmission = transmission.split("\x04")[0]
            return transmission
    raise Exception("Faulty Transmission!")


print(''.join(str(i) for i in [1, 2, 3]) in ''.join(str(i) for i in [1, 2, 3, 4]))

result = read_wave("lol.test.wav")

while len(result) % 16:
    result.append(0)

for i in range(16):
    s = ""
    for i in range(len(result) // 16 + 1):
        r = result[i*16:i*16+16]
        if r:
            s += chr(int(''.join(str(i) for i in r), 2))
    if "\x02" in s and "\x04" in s:
        print(s)
        print(s)
        print(s)
    result = result[-1:] + result[0:-1]
