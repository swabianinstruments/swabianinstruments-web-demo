# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 09:11:22 2020

@author: liu
"""


from time import sleep
from TimeTagger import createTimeTagger, freeAllTimeTagger, Coincidence, Countrate

# create a Time Tagger instance
tagger = createTimeTagger()
tagger.reset()

# sets test signal to channels 1, 2, and 3
tagger.setTestSignal([1, 2, 3], True)
tagger.sync()
print('\nTest signal is activated at channels 1, 2, and 3.')

# run the triple-coincidence measurement
# cw = coincidence window
# play with coincidence window and notice chanes in the countrate
# alternatively, introduce delays at channels [1, 2, 3] to change the result
cw = 450 # ps
coinc = Coincidence(tagger, [1, 2, 3], cw)
coinc_channel = coinc.getChannel()
print(f'\nCoincidence is assigned to virtual channel {coinc_channel}.')

# measure average countrate in counts per second on all channels
cr = Countrate(tagger, [1, 2, 3, coinc_channel])
sleep(1.0) # collect data for 1 s
cr_data = cr.getData()
cr1 = cr_data[0]
cr2 = cr_data[1]
cr3 = cr_data[2]
cr_coinc = cr_data[3]

# display the countrates
print(f'\nCountrate on channel 1 is {int(cr1)} cps.')
print(f'Countrate on channel 2 is {int(cr2)} cps.')
print(f'Countrate on channel 3 is {int(cr3)} cps.')
print(f'\nCountrate on coincidence channel is {int(cr_coinc)} cps.')

# release the Time Tagger
freeAllTimeTagger()