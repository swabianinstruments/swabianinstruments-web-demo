# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 09:21:02 2020

@author: liudm
"""

import numpy as np
import random as rnd
from time import sleep


def LASERpattern(f, ln):
    """ defines laser pattern with repetition rate f MHz
        ln is the length of pattern
    """

    period = round(1/f/1e6*1e9) # ns between laser pulses
    pattern = [(1, 1), (period-1, 0)]
    # extend up to length "ln"
    for i in range(1,ln):
        pattern.append((1, 1))
        pattern.append((period-1, 0))
    return pattern


def PHOTONpattern(f, tau, ln):
    """ defines photon pattern following the excitation at f MHz
        probability of photon emission is such that photon rate is around 1 MHz
        ln is the length of pattern
    """

    period = round(1/f/1e6*1e9) # ns between laser pulses
    prob = 1/f
    # generate a random time stamp
    a = (period-1)/(np.exp(1/tau)-1)
    stamp = int(a * (np.exp(rnd.random()/tau) - 1) + 1)
    # add the stamp to pattern accorging to probability
    if (rnd.random() < prob):
        if (stamp == 1):
            pattern = [(1, 1), (period-1, 0)]
        elif (stamp == period):
            pattern = [(period-1, 0), (1, 1)]
        else:
            pattern = [(stamp-1, 0), (1, 1), (period-stamp, 0)]
    else:
        pattern = [(period, 0)]
    # extend the pattern up to length "ln"
    for i in range (1, ln):
        stamp = int(a * (np.exp(rnd.random()/tau) - 1) + 1)
        if (rnd.random() < prob):
            if (stamp == 1):
                pattern.append((1, 1))
                pattern.append((period-1, 0))
            elif (stamp == period):
                pattern.append((period-1, 0))
                pattern.append((1, 1))
            else:
                pattern.append((stamp-1, 0))
                pattern.append((1, 1))
                pattern.append((period-stamp, 0))
        else:
            pattern.append((period, 0))
    return pattern
    

def main(pulsestreamer_ip='169.254.8.2'):
    """ This is the main function of the example.
        Parameters: 
            pulsestreamer_ip -  IP address of the Pulse Streamer.
                                The default value corresponds to the
                                direct connection of the Pulse Streamer 
                                to the network card of your PC.
    """

    # import Pulse Streamer API into the current namespace
    from pulsestreamer import PulseStreamer

    # connect to the Pulse Streamer
    ps = PulseStreamer(pulsestreamer_ip)

    # create a sequence-object
    sequence = ps.createSequence()

    # choose parameters
    # las_f - laser repetition rate in MHz
    # pl_tau - non-dimentional photoluminescence lifetime
    # (pl_tau/las_f*1e3) = lifetime in ns
    # patt_ln is length of one pattern
    las_f = 80
    pl_tau = 0.4
    patt_ln = 1000

    hold = 0.2 # seconds
    runs = PulseStreamer.REPEAT_INFINITELY
    ps.stream(sequence, runs)
    while True:
        # generate patterns
        pattern1 = LASERpattern(las_f, patt_ln)
        pattern2 = PHOTONpattern(las_f, pl_tau, patt_ln)
        # assign the patterns to digital channels
        sequence.setDigital(1, pattern1)
        sequence.setDigital(2, pattern2)
        sleep(hold)
        ps.stream(sequence, runs)
        
        

if __name__ == '__main__':
    main()