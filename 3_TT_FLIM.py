# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:01:41 2020

@author: liudm
"""

from time import sleep
import plot_TT

from TimeTagger import createTimeTagger, freeAllTimeTagger, TimeDifferences

# create a Time Tagger instance
tagger = createTimeTagger()
tagger.reset()

# assign channels for measurement
phot_ch = 1
strt_ch = 2
next_ch = 3
sync_ch = 4

# initialize measurement parameters
binwidth = 10000 # 10 ns
bins = 100
n_pix = 10

# measure FLIM
image = TimeDifferences(tagger, phot_ch, strt_ch, next_ch, sync_ch, binwidth, bins, n_pix)
print("\nFLIM measurement is running.")
sleep(20)
xFLIM = image.getIndex()
yFLIM = image.getData()
plot_TT.BarChart2D(xFLIM, yFLIM)

# free the Time Tagger
freeAllTimeTagger()

