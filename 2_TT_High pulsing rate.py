# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:01:41 2020

@author: liu

"""

NAME = 'High Pulsing Rate'
DESCR = """
This example uses **Time Tagger** to emulate time-resolved 
fluorescence measurement with high laser repetition rate.

* Channel 1 - fluorescence photons
* Channel 2 - laser pulses 

"""

from time import sleep
import plot_TT

from TimeTagger import createTimeTagger, freeAllTimeTagger, Countrate, Histogram

# create a Time Tagger instance
tagger = createTimeTagger()
tagger.reset()

# measure countrate at channels 1 and 2
phot_ch = 1
las_ch = 2
cr = Countrate(tagger, [las_ch, phot_ch])
sleep(1)
cr_las, cr_phot = cr.getData()
print(f"\nCountrate on channel {las_ch} is {int(cr_las)} cps")
print(f"Countrate on channel {phot_ch} is {int(cr_phot)} cps")
cr.stop()

# set up conditional filter
tagger.setConditionalFilter([phot_ch], [las_ch])
tagger.sync()
overfl = tagger.getOverflowsAndClear()
print(f"\nOverflows: {overfl}")
print(f"\nSetting up Conditional Filter for channel {las_ch}")

# measure the countrates again after applying conditional filter
cr.startFor(int(1e12))
sleep(1)
cr_las, cr_phot = cr.getData()
print(f"\nCountrate on channel {las_ch} is {int(cr_las)} cps")
print(f"Countrate on channel {phot_ch} is {int(cr_phot)} cps")
cr.stop()
overfl = tagger.getOverflowsAndClear()
print(f"\nOverflows: {overfl}")

# collect time-resolved fluorescence for 10 seconds
binwidth = 1000 # 1 ns
bins = 13
# mind that now start=photon, click=laser
hist = Histogram(tagger, las_ch, phot_ch, binwidth, bins)
print("\nHistogram measurement is running.")
sleep(10)
# flip the histogram along the time-axis
xhist = abs(hist.getIndex()-bins*1000)
yhist = hist.getData()
plot_TT.BarChart(xhist, yhist)
freeAllTimeTagger()

