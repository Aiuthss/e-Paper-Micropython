#!/usr/bin/python
# -*- coding:utf-8 -*-
# *****************************************************************************
# * | File        :	  epd5in65f.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2020-03-02
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import gc
import time
import machine

CS_PIN          = 15
DC_PIN          = 27
RST_PIN         = 26
BUSY_PIN        = 25

hspi = machine.SPI(1, 10000000, sck=machine.Pin(14), mosi=machine.Pin(13), miso=machine.Pin(12))

def to_byte(data):
    if type(data) is list:
        x = bytearray(len(data))
        for i, content in enumerate(data):
            x[i] = content
    elif type(data) is bytes:
        x = data
    else:
        x = bytearray(1)
        x[0] = data
    return x

def digital_write(pin, value):
    p0 = machine.Pin(pin, machine.Pin.OUT)
    p0.value(value)

def digital_read(pin):
    p0 = machine.Pin(pin, machine.Pin.IN)
    return p0.value()

def delay_ms(delaytime):
    time.sleep(delaytime / 1000.0)

def spi_writebyte(data):
    hspi.write(to_byte(data))

def module_exit(self):
    print("spi end")
    hspi.deinit()
    print("close 5V, Module enters 0 power consumption ...")
    p0 = machine.Pin(RST_PIN, machine.Pin.OUT)
    p1 = machine.Pin(DC_PIN, machine.Pin.OUT)
    p0.value(0)
    p1.value(0)

# Display resolution
EPD_WIDTH       = 600
EPD_HEIGHT      = 448

class EPD:
    def __init__(self):
        self.reset_pin = RST_PIN
        self.dc_pin = DC_PIN
        self.busy_pin = BUSY_PIN
        self.cs_pin = CS_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.BLACK  = 0x000000   #   0000  BGR
        self.WHITE  = 0xffffff   #   0001
        self.GREEN  = 0x00ff00   #   0010
        self.BLUE   = 0xff0000   #   0011
        self.RED    = 0x0000ff   #   0100
        self.YELLOW = 0x00ffff   #   0101
        self.ORANGE = 0x0080ff   #   0110


    # Hardware reset
    def reset(self):
        digital_write(self.reset_pin, 1)
        delay_ms(600)
        digital_write(self.reset_pin, 0)
        delay_ms(2)
        digital_write(self.reset_pin, 1)
        delay_ms(200)

    def send_command(self, command):
        digital_write(self.dc_pin, 0)
        digital_write(self.cs_pin, 0)
        spi_writebyte(command)
        digital_write(self.cs_pin, 1)

    def send_data(self, data):
        digital_write(self.dc_pin, 1)
        digital_write(self.cs_pin, 0)
        spi_writebyte(data)
        digital_write(self.cs_pin, 1)


    def read_send_data(self, s, size):
        digital_write(self.dc_pin, 1)
        digital_write(self.cs_pin, 0)
        while True:
            gc.collect()
            letters = s.read(size)
            if letters and letters != b'':
                spi_writebyte(letters)
            else:
                print('close')
                s.close()
                break
        digital_write(self.cs_pin, 1)

    #def send_files(self, files):
    #    digital_write(self.dc_pin, 1)
    #    digital_write(self.cs_pin, 0)
    #    for file in files:
    #        f = open(file, 'rb')
    #        data = f.read()
    #        spi_writebyte(data)
    #    spi_writebyte(data)
    #    digital_write(self.cs_pin, 1)        

    def ReadBusyHigh(self):
        print("e-Paper busy")
        while(digital_read(self.busy_pin) == 0):      # 0: idle, 1: busy
            delay_ms(100)
        print("e-Paper busy release")

    def ReadBusyLow(self):
        print("e-Paper busy")
        while(digital_read(self.busy_pin) == 1):      # 0: idle, 1: busy
            delay_ms(100)
        print("e-Paper busy release")

    def init(self):
        # EPD hardware init start
        self.reset()
        print("reset")
        self.ReadBusyHigh()
        self.send_command(0x00)
        self.send_data(0xEF)
        self.send_data(0x08)
        self.send_command(0x01)
        self.send_data(0x37)
        self.send_data(0x00)
        self.send_data(0x23)
        self.send_data(0x23)
        self.send_command(0x03)
        self.send_data(0x00)
        self.send_command(0x06)
        self.send_data(0xC7)
        self.send_data(0xC7)
        self.send_data(0x1D)
        self.send_command(0x30)
        self.send_data(0x3c)
        self.send_command(0x41)
        self.send_data(0x00)
        self.send_command(0x50)
        self.send_data(0x37)
        self.send_command(0x60)
        self.send_data(0x22)
        self.send_command(0x61)
        self.send_data(0x02)
        self.send_data(0x58)
        self.send_data(0x01)
        self.send_data(0xC0)
        self.send_command(0xE3)
        self.send_data(0xAA)

        delay_ms(100)
        self.send_command(0x50)
        self.send_data(0x37)
        print("init fin")

    #def display(self,image):
    #    self.send_command(0x61) #Set Resolution setting
    #    self.send_data(0x02)
    #    self.send_data(0x58)
    #    self.send_data(0x01)
    #    self.send_data(0xC0)
    #    self.send_command(0x10)
#
    #    self.send_data(image)
    #    self.send_command(0x04) #0x04
    #    self.ReadBusyHigh()
    #    self.send_command(0x12) #0x12
    #    self.ReadBusyHigh()
    #    self.send_command(0x02) #0x02
    #    self.ReadBusyLow()
    #    delay_ms(500)

    def read_display(self, http, size):
        self.send_command(0x61) #Set Resolution setting
        self.send_data(0x02)
        self.send_data(0x58)
        self.send_data(0x01)
        self.send_data(0xC0)
        self.send_command(0x10)

        self.read_send_data(http.s, size)
        #データを送り終えたらネットワークインタフェースを無効化
        http.wlan.active(False)
        print('network interface inactivated')
        self.send_command(0x04) #0x04
        self.ReadBusyHigh()
        self.send_command(0x12) #0x12
        self.ReadBusyHigh()
        self.send_command(0x02) #0x02
        self.ReadBusyLow()
        delay_ms(500)

    def Clear(self):
        self.send_command(0x61) #Set Resolution setting
        self.send_data(0x02)
        self.send_data(0x58)
        self.send_data(0x01)
        self.send_data(0xC0)
        self.send_command(0x10)

        # Set all pixels to white
        for i in range(0, self.height):
            buf = bytes([0x11] * int(self.width / 2))
            self.send_data(buf)

        self.send_command(0x04) #0x04
        self.ReadBusyHigh()
        self.send_command(0x12) #0x12
        self.ReadBusyHigh()
        self.send_command(0x02) #0x02
        self.ReadBusyLow()
        delay_ms(500)

    def sleep(self):
        delay_ms(500)
        self.send_command(0x07) # DEEP_SLEEP
        self.send_data(0XA5)
        digital_write(self.reset_pin, 0)

        delay_ms(2000)
        module_exit()
