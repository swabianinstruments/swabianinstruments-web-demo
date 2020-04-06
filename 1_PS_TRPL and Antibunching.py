# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 14:58:24 2020

@author: liu
"""
import numpy as np
import random as rnd
from time import sleep

# function that returns a time tag in ns
# with statistics of monoexponential photoluminescece decay
# the window is indirectly defined by variable "amplitude"
# variable "time" is random in the range [0,1]
def TRPLtag(time, lifetime, amplitude):
    time_tag = int(amplitude * (np.exp(time/lifetime) - 1) + 1)
    return time_tag

# function that creates a pattern imitating time-resolved photoluminescence
# returns a pattern with one randomly generated photon tag within window "wind"
# tau - exponential lifetime of TRPL
# wind - measurement window in ns
def TRPLpattern(tau, wind, rep):
    a = (wind - 1)/(np.exp(1/tau)-1)
    f = TRPLtag(rnd.random(), tau, a)
    if (f == 1):
        pattern_PL = [(1, 1)]
        pattern_PL.append((wind-1, 0))
    elif (f == wind):
        pattern_PL = [(wind-1, 0)]
        pattern_PL.append((wind, 1))
    else:
        pattern_PL = [(f-1, 0)]
        pattern_PL.append((1, 1))
        pattern_PL.append((wind-f, 0))
    for i in range(1,rep):
        f = TRPLtag(rnd.random(), tau, a)
        if (f == 1):
            pattern_PL.append((1, 1))
            pattern_PL.append((wind-1, 0))
        elif (f == wind):
            pattern_PL.append((wind-1, 0))
            pattern_PL.append((wind, 1))
        else:
            pattern_PL.append((f-1, 0))
            pattern_PL.append((1, 1))
            pattern_PL.append((wind-f, 0))
    return pattern_PL

# function that creates a pattern imitating pulsed excitation
# "wind" is period between the pulses in ns
def LASERpattern(period, rep):
    pattern_las = [(1, 1), (period-1, 0)]
    for i in range(1,rep):
        pattern_las.append((1, 1))
        pattern_las.append((period-1, 0))
    return pattern_las

# function that imitates photon antibunching measurement with CW excitation
# returns two patterns for two detectors
# "coi" is coincidence degree, that is if coi = 0.2
# then 40% of photons get only to det1; 40% go only to det2; 20% go to both
def ANTIBpattern(per, rep):
    # generate a photon count
    f = round(rnd.random()*(per - 1)) + 1
    # imitate 50% photon splitter
    if (rnd.random() < 0.5):
        if (f == 1):
            patt_det1 = [(1, 1)]
            patt_det1.append((per-1, 0))
        elif (f == per):
            patt_det1 = [(per-1, 0)]
            patt_det1.append((1, 1))
        else:
            patt_det1 = [(f-1, 0)]
            patt_det1.append((1, 1))
            patt_det1.append((per-f, 0))
        patt_det2 = [(per, 0)]
    else:
        patt_det1 = [(per, 0)]
        if (f == 1):
            patt_det2 = [(1, 1)]
            patt_det2.append((per-1, 0))
        elif (f == per):
            patt_det2 = [(per-1, 0)]
            patt_det2.append((1, 1))
        else:
            patt_det2 = [(f-1, 0)]
            patt_det2.append((1, 1))
            patt_det2.append((per-f, 0))
    # repeat for "rep" repetitions
    # imitate 50% photon splitter
    for i in range(1, rep):
        f = round(rnd.random()*(per - 1)) + 1
        if (rnd.random() < 0.5):
            if (f == 1):
                patt_det1.append((1, 1))
                patt_det1.append((per-1, 0))
            elif (f == per):
                patt_det1.append((per-1, 0))
                patt_det1.append((1, 1))
            else:
                patt_det1.append((f-1, 0))
                patt_det1.append((1, 1))
                patt_det1.append((per-f, 0))
            patt_det2.append((per, 0))
        else:
            patt_det1.append((per, 0))
            if (f == 1):
                patt_det2.append((1, 1))
                patt_det2.append((per-1, 0))
            elif (f == per):
                patt_det2.append((per-1, 0))
                patt_det2.append((1, 1))
            else:
                patt_det2.append((f-1, 0))
                patt_det2.append((1, 1))
                patt_det2.append((per-f, 0))
    return patt_det1, patt_det2

# import API classes into the current namespace
from pulsestreamer import PulseStreamer

# IP of Pulse Streamer connected directly by Ethernet cable
ip = '169.254.8.2'

# connect to the Pulse Streamer
ps = PulseStreamer(ip)

# create a sequence-object
sequence = ps.createSequence()

# choose your parameters
# lifetime of photoluminescence
# non-dimentional normalized factor
# multiply by "window" to get lifetime in ns
exp_tau = 0.37
# window is period between laser pulses
# for Time Tagger 20 choose window >= 500 ns (below 2 MHz on 1 channel)
# for Time Tagger Ultra choose window >= 50 ns (below 20 MHz on 1 channel)
window = 1000 # ns
# repeat = repetitions per one pattern
repeat = 1000

hold = 0.2 # seconds
n_runs = PulseStreamer.REPEAT_INFINITELY
# generate new patterns interminably
# and hold each new pattern for time "hold"
while (True):
    # TRPL pattern for channels 1 and 2
    pattern1 = LASERpattern(window, repeat)
    pattern2 = TRPLpattern(exp_tau, window, repeat)
    # antibunching pattern for channels 3 and 4
    antibunching = ANTIBpattern(int(window/10), repeat)
    pattern3 = antibunching[0]
    pattern4 = antibunching[1]
    # assign the pattern to the digital channels
    sequence.setDigital(1, pattern1)
    sequence.setDigital(2, pattern2)
    sequence.setDigital(3, pattern3)
    sequence.setDigital(4, pattern4)
    # stream the sequence and repeat it infinitely
    sleep(hold)
    ps.stream(sequence, n_runs)
