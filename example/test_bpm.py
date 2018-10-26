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
from max30100 import MAX30100, PULSE_WIDTH, SAMPLE_RATE
from max30100.filters import median_filter,bpm_filter,maxmin_filter
from max30100.filters import freq_filter,resample_filter,avg_filter,median_filter,bpm_filter
from max30100.filters import hysteresis_filter,mean_filter,norm_filter,butterworth_filter
from max30100.filters import adc_gen,derivative_filter,thresh_filter,diff_filter


import pyb

def rec():
    h = MAX30100(sample_rate=SAMPLE_RATE[100], pulse_width=PULSE_WIDTH[1600])

    with open("/sd/pulse_max30100.csv", "w") as f:
        first = True

        g = h.generator(delay=8)  # 10ms <> 100sps
        # med = median_filter(g,15)
        bw = butterworth_filter(g)

        norm = norm_filter(bw, size=100)
        diff = diff_filter(norm, size=20)
        th = thresh_filter(diff, threshold=-.33, greater_than=False)
        # th = hysteresis_filter(bw,size=100,th_high=.7,th_low=.3)

        bpm = bpm_filter(th, size=3)

        for s, v, h in bpm:
            if first:
                col_names = ",".join(h.keys())
                f.write("%s\n" % col_names)
                first = False

            print(h)
            s = ','.join([str(v) for v in h.values()])
            f.write("%s\n" % s)

            if h['thresh']:
                pyb.LED(1).on()
            else:
                pyb.LED(1).off()
            # lcd.clear()
            # lcd.write(str(h))
            # if keys.read() is not 'none':
            #     break
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
