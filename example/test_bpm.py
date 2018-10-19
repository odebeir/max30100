""""
  PyBoard library for generator based filters
  https://github.com/odebeir/max30100

MIT License

Copyright (c) 2018 Olivier Debeir

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from max30100 import MAX30100
from max30100.filters import median_filter,bpm_filter,maxmin_filter
import pyb

def rec():

    h = MAX30100()
    g = h.generator(25)
    with open("/sd/pulse_max30100.csv", "w") as f:
        f.write("temp,bpm,red,adc,med,trig,max,min\n")
        for s, v, h in bpm_filter(maxmin_filter(median_filter(g, 5), size=40, th_low=.4, th_high=.70)):
            print(h)
            f.write("%f,%f,%d,%d,%d,%d,%d,%d\n" % (
            h['temp'], h['bpm'], h['red'], h['adc'], h['med'], h['trig'], h['max'], h['min']))
            if h['trig']:
                pyb.LED(1).on()
            else:
                pyb.LED(1).off()
        f.close()
        pyb.sync()

def test():

    h = MAX30100()
    g = h.generator(25)
    for s, v, h in bpm_filter(maxmin_filter(median_filter(g, 5), size=40, th_low=.4, th_high=.70)):
        print(h)
        if h['trig']:
            pyb.LED(1).on()
        else:
            pyb.LED(1).off()
