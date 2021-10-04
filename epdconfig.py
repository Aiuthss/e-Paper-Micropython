# /*****************************************************************************
# * | File        :	  epdconfig.py
# * | Author      :   Waveshare team
# * | Function    :   Hardware underlying interface
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2019-06-21
# * | Info        :   
# ******************************************************************************
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

import time
import machine

class ESP32:
    # Pin definition
    DC_PIN          = 15
    CS_PIN          = 27
    RST_PIN         = 26
    BUSY_PIN        = 25

    def __init__(self):
        # MOSI: 13, SCLK: 14, CS: 15
        self.hspi = machine.SPI(1, 10000000)

    def digital_write(self, pin, value):
        p0 = machine.Pin(pin, machine.Pin.OUT)
        p0.value(value)

    def digital_read(self, pin):
        p0 = machine.Pin(pin, machine.Pin.IN)
        return p0.value()

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.hspi.write(bytes(data))

    def module_exit(self):
        print("spi end")
        self.hspi.deinit()

        print("close 5V, Module enters 0 power consumption ...")
        p0 = machine.Pin(self.RST_PIN, machine.Pin.OUT)
        p1 = machine.Pin(self.DC_PIN, machine.Pin.OUT)
        p0.value(0)
        p1.value(0)