# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:01:41 2020

@author: liudm
"""

from time import sleep
import plot_TT

from TimeTagger import createTimeTagger, freeAllTimeTagger, Countrate, Histogram

# create a Time Tagger instance
tagger = createTimeTagger()
tagger.reset()

# measure countrate on channels 1 and 2
las_ch = 1
phot_ch = 2
cr = Countrate(tagger, [las_ch, phot_ch])
sleep(1.0)
cr_las, cr_phot = cr.getData()
print("\nCountrate on channel ", las_ch, " is ", int(cr_las), "cps")
print("Countrate on channel ", phot_ch, " is ", int(cr_phot), "cps")
cr.stop()

# set up conditional filter
tagger.setConditionalFilter([phot_ch], [las_ch])
tagger.sync()
overfl = tagger.getOverflowsAndClear()
print("\nOverflows: ", overfl)
print("\nSetting up Conditional Filter for channel ", las_ch)

# measure the countrates again after applying conditional filter
cr.startFor(int(1e12))
sleep(1.0)
cr_las, cr_phot = cr.getData()
print("\nCountrate on channel ", las_ch, " is ", int(cr_las), "cps")
print("Countrate on channel ", phot_ch, " is ", int(cr_phot), "cps")
cr.stop()
overfl = tagger.getOverflowsAndClear()
print("\nOverflows: ", overfl)

# measure time-resolved photoluminescence
binwidth = 1000 # 1 ns
bins = 13
hist = Histogram(tagger, las_ch, phot_ch, binwidth, bins)
print("\nHistogram measurement is running.")
sleep(20)
xhist = abs(hist.getIndex()-bins*1000)
yhist = hist.getData()
plot_TT.BarChart(xhist, yhist)
freeAllTimeTagger()

