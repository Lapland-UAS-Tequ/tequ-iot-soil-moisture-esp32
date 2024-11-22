'''
The MIT License (MIT)

Copyright (c) 2018-2019 Rafael Römhild

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''


import ustruct
import ubinascii

def decode_data_format_2and4(data):
    """RuuviTag URL decoder"""
    data = data.encode()
    identifier = None
    if len(data) > 8:
        identifier = data[8]
        data = data[:8]
    decoded = ubinascii.a2b_base64(data)

    data_format = decoded[0]
    humidity = decoded[1] / 2
    temperature = (decoded[2] & 127) + decoded[3] / 100
    pressure = ((decoded[4] << 8) + decoded[5]) + 50000

    return (data_format, humidity, temperature, pressure, identifier)


def decode_data_format_3(data):
    """RuuviTag RAW 1 decoder"""
    humidity = data[3] / 2

    temperature = data[4] + data[5] / 100
    if temperature > 128:
        temperature -= 128
        temperature = round(0 - temperature, 2)

    pressure = ustruct.unpack("!H", data[6:8])[0] + 50000
    acceleration_x = ustruct.unpack("!h", data[8:10])[0]
    acceleration_y = ustruct.unpack("!h", data[10:12])[0]
    acceleration_z = ustruct.unpack("!h", data[12:14])[0]
    battery_voltage = ustruct.unpack("!H", data[14:16])[0]

    return (
        3,
        humidity,
        temperature,
        pressure,
        acceleration_x,
        acceleration_y,
        acceleration_z,
        battery_voltage,
    )


def decode_data_format_5(data):
    """RuuviTag RAW 2 decoder"""
    temperature = ustruct.unpack("!h", data[3:5])[0] * 0.005
    humidity = ustruct.unpack("!H", data[5:7])[0] * 0.0025
    pressure = ustruct.unpack("!H", data[7:9])[0] + 50000
    acceleration_x = ustruct.unpack("!h", data[9:11])[0]
    acceleration_y = ustruct.unpack("!h", data[11:13])[0]
    acceleration_z = ustruct.unpack("!h", data[13:15])[0]
    power_bin = bin(ustruct.unpack("!H", data[15:17])[0])[2:]
    battery_voltage = int(power_bin[:11], 2) + 1600
    tx_power = int(power_bin[11:], 2) * 2 - 40
    movement_counter = data[18]
    measurement_sequence = ustruct.unpack("!H", data[18:20])[0]

    return (
        5,
        humidity,
        temperature,
        pressure,
        acceleration_x,
        acceleration_y,
        acceleration_z,
        battery_voltage,
        tx_power,
        movement_counter,
        measurement_sequence,
    )

def decode_data(data_format, data):
    if data_format in (2, 4):
        return decode_data_format_2and4(data)
    elif data_format == 3:
        return decode_data_format_3(data)
    elif data_format == 5:
        return decode_data_format_5(data)