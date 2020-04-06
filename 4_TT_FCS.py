# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 16:47:21 2020

@author: liudm
"""

from time import sleep
import plot_TT

from TimeTagger import createTimeTagger, freeAllTimeTagger, HistogramLogBins
    
# create a Time Tagger instance
tagger = createTimeTagger()
tagger.reset()

# measure FCS by start-stop histogram with logarithmic binning
ch = 1

bins = 100 # algoritm complexity increases as square of bins
left = -6 # left boarder of measurment window is 1^left in seconds
right = 0 # right boarder of measurement window is 1^right in seconds
hist = HistogramLogBins(tagger, ch, ch, left, right, bins)
print("\nHistogram measurement is running.")

# collect data for 5 seconds and plot
sleep(10.0)
# start-stop histogram -> TRPL data
bins = hist.getBinEdges()
y = hist.getDataNormalizedG2()
plot_TT.ScatterLogBinsPlot(bins, y, left, right)

# terminate the open connection to the Time Tagger
freeAllTimeTagger()