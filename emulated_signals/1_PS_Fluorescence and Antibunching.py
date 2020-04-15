# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 14:58:24 2020

@author: liu
"""


NAME = 'Fluorescence and Antibunching'
DESCR = """
This example uses **Pulse Streamer** to emulate signals for a typical time-resolved 
fluorescence measurement and for photon antibunching under steady-state excitation.
The script generates the folowing signals

* Channel 1 - fluorescence photons
* Channel 2 - laser pulses
* Channel 3 and Channel 4 - photons with antibunching properties
"""

import numpy as np
import random as rnd
from time import sleep



def TRFLtag(time, lifetime, amplitude):
    """ function that returns a time tag in ns
        with statistics of smooth fluorescence decay
        the window is indirectly defined by variable "amplitude"
        variable "time" is random in the range [0,1]
    """
    time_tag = int(round((amplitude * (np.exp(time/lifetime) - 1) + 1)))
    return time_tag


def TRFLpattern(tau, wind, rep):
    """ function that creates a pattern imitating time-resolved fluorescence
        returns a pattern with one randomly generated photon tag within window "wind"
        tau - approximate fluorescence lifetime
        wind - measurement window in ns
    """
    
    # calculate constant "a" for random generation
    a = (wind - 1)/(np.exp(1/tau)-1)
    # initialize pattern
    pattern_FL = [(0, 0)]
    for i in range(rep):
        pattern_FL.append((1, 0))
        f = TRFLtag(rnd.random(), tau, a)
        if (f == 1):
            pattern_FL.append((1, 1))
            pattern_FL.append((wind-2, 0))
        elif (f == wind):
            pattern_FL.append((wind-2, 0))
            pattern_FL.append((1, 1))
        else:
            pattern_FL.append((f-1, 0))
            pattern_FL.append((1, 1))
            pattern_FL.append((wind-1-f, 0))
    return pattern_FL


def LASERpattern(period, rep):
    """function that creates a pattern imitating pulsed laser excitation
        rep - pulses within the pattern
        period between the pulses is in ns
    """
    pattern_las = [(1, 1), (period-1, 0)]
    for i in range(1,rep):
        pattern_las.append((1, 1))
        pattern_las.append((period-1, 0))
    return pattern_las


def ANTIBpattern(per, rep):
    """ function that imitates photon antibunching measurement with CW excitation
        returns two patterns for two detectors
        photon goes to one of the detectors with 50% probability
    """

    # initialize patterns
    patt_det1 = [(0, 0)]
    patt_det2 = [(0, 0)]
    # generate "rep" photons
    for i in range(rep):
        # generate one photon count at random moment within period "per"
        f = round(rnd.random()*(per - 1)) + 1
        # imitate 50% photon splitter
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


def main(pulsestreamer_ip='169.254.8.2'):
    """ This is the main function of the example.
        Parameters: 
            pulsestreamer_ip -  IP address of the Pulse Streamer.
                                The default value corresponds to the
                                direct connection of the Pulse Streamer 
                                to the network card of your PC.
    """

    # import API classes into the current namespace
    from pulsestreamer import PulseStreamer
    
    # connect to the Pulse Streamer
    ps = PulseStreamer(pulsestreamer_ip)
    ps.reset()
    
    # create a sequence-object
    sequence = ps.createSequence()
    
    # choose your parameters
    # approximate fluorescence lifetime
    # non-dimentional normalized factor
    # multiply by "window" to get lifetime in ns
    exp_tau = 0.37
    # window is period between laser pulses
    # for Time Tagger 20 choose window >= 500 ns (below 2 MHz at 1 channel)
    # for Time Tagger Ultra choose window >= 50 ns (below 20 MHz at 1 channel)
    window = 1000 # ns
    # repeat = repetitions per one pattern
    repeat = 1000
    
    hold = 0.2 # seconds
    n_runs = PulseStreamer.REPEAT_INFINITELY
    # generate new patterns interminably
    # and hold each new pattern for time "hold"
    while (True):
        # TRFL pattern for channels 1 and 2
        pattern1 = TRFLpattern(exp_tau, window, repeat)
        pattern2 = LASERpattern(window, repeat)
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


if __name__ == '__main__':
    main()