# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 09:21:02 2020

@author: liu
"""

NAME = 'High Pulsing Rate'
DESCR = """
This example uses **Pulse Streamer** to emulate signals for a time-resolved 
fluorescence measurement with high laser repetition rate.

* Channel 1 - fluorescence photons
* Channel 2 - laser pulses 

"""

import numpy as np
import random as rnd
from time import sleep


def LASERpattern(f, ln):
    """ defines laser pattern with repetition rate f MHz
        ln is the length of pattern
    """

    period = int(round(1/f/1e6*1e9)) # ns between laser pulses
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

    period = int(round(1/f/1e6*1e9)) # ns between laser pulses
    # initialize a photon pattern
    pattern = [(0, 0)]
    # constant amplitude for random photon generation
    # choose a < 1
    a = 0.05
    # generate the pattern of length "ln"
    for i in range(ln):
        pattern.append((1, 0))
        # generate a random time stamp
        t = rnd.randint(1, period-1)
        # probability of this stamp to appear in the pattern
        prob = rnd.random()
        # add the stamp to pattern accorging to probability
        if ( prob < ( a * np.exp(-(t-1)/tau) ) ):
            if (t == 1):
                pattern.append((1, 1))
                pattern.append((period-2, 0))
            elif (t == (period-1)):
                pattern.append((period-2, 0))
                pattern.append((1, 1))
            else:
                pattern.append((t-1, 0))
                pattern.append((1, 1))
                pattern.append((period-1-t, 0))
        else:
            pattern.append((period-1, 0))
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
    # pl_tau - fluorescence lifetime in ns
    # patt_ln is length of one pattern
    las_f = 80
    pl_tau = 4
    patt_ln = 1000

    hold = 0.2 # seconds
    runs = PulseStreamer.REPEAT_INFINITELY
    ps.stream(sequence, runs)
    while True:
        # generate patterns
        pattern1 = PHOTONpattern(las_f, pl_tau, patt_ln)
        pattern2 = LASERpattern(las_f, patt_ln)
        # assign the patterns to digital channels
        sequence.setDigital(1, pattern1)
        sequence.setDigital(2, pattern2)
        sleep(hold)
        ps.stream(sequence, runs)
        
        

if __name__ == '__main__':
    main()