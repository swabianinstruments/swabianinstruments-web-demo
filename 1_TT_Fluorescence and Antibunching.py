# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 13:47:26 2020

@author: liu
"""

from time import sleep
import plot_TT

from TimeTagger import createTimeTagger, freeAllTimeTagger, Histogram, Correlation
    
# create a Time Tagger instance
tagger = createTimeTagger()
tagger.reset()

# measure time-resolved fluorescence
click_ch = 1 # photon count at 1st channel
start_ch = 2 # laser pulse at 2nd channel
binwidth = 1000 # 1 ns
bins = 1000
hist = Histogram(tagger, click_ch, start_ch, binwidth, bins)
print("\nHistogram measurement is running.")

# measure photon antibunching
corr_ch1 = 3 # first photon channel for antubunching measurements
corr_ch2 = 4 # second photon channel for antibunching measurements
bwcorr = 1000 # 1 ns
nbins = 1000
corr = Correlation(tagger, corr_ch1, corr_ch2, bwcorr, nbins)
print("\nCorrelation measurement is running.")

# collect data for 10 seconds and plot
sleep(10)
# start-stop histogram -> TRFL data
xhist = hist.getIndex()
yhist = hist.getData()
plot_TT.ScatterPlot(xhist, yhist)
plot_TT.ScatterLogPlot(xhist, yhist)
# normalized correlation -> Photon Antibunching
xcorr = corr.getIndex()
ycorr = corr.getDataNormalized()
plot_TT.LinePlot(xcorr, ycorr)

# terminate the open connection to the Time Tagger
freeAllTimeTagger()