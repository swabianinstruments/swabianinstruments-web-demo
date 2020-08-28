# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:19:50 2020

@author: liu

"""


NAME = 'FLIM'
DESCR = """
This example uses **Pulse Streamer** to emulate signals for fluorescence lifetime imaging (FLIM).
Laser pulse serves as a start count;
fluorescence photon is a stop count;
pixel count moves to the next histogram (next FLIM pixel);
sync count returns measurement to the beginning of the FLIM-image.

* Channel 1 - fluorescence photon
* Channel 2 - laser pulse
* Channel 3 - pixel count
* Channel 4 - sync count

"""

import numpy as np
import random as rnd

# tag distribution to emulate exponential fluorescence decay
def expFL(tau, binwidth, bins, counts):
    distr = [np.exp(-0/tau)]
    for i in range(1, bins):
        distr.append(np.exp(-i*binwidth/tau))
    fact = counts/np.sum(distr)
    for i in range(bins):
        distr[i] = fact*distr[i]
        distr[i] = int(round(distr[i]))
    while (np.sum(distr) > counts):
        if (distr[-1] != 0):
            ind = len(distr) - 1
        else:
            ind = distr.index(0) - 1
        distr[ind] = distr[ind] - 1
    return distr

# generate a randomized FLIM pattern
def genFLIM(pl_lt, las_period, pix_period):
    pix_pattern = [(1, 1), (pix_period, 0)]
    las_pattern = [(1, 0), (1, 1), (las_period - 1, 0)]
    las_counts = int(pix_period/las_period)
    for i in range(1, las_counts):
        las_pattern.append((1, 1))
        las_pattern.append((las_period - 1, 0))
    bw = 10
    bns = 100
    phot_distr = expFL(pl_lt, bw, bns, las_counts)
    phot_pattern = [(1, 0)]
    for b in range(phot_distr[0]):
        phot_pattern.append((1, 0))
        phot_pattern.append((1, 1))
        phot_pattern.append((las_period - 2, 0))
    p = 1
    while ((phot_distr[p] > 0) and (p < (bns-1))):
        for b in range(phot_distr[p]):
            phot_pattern.append((1, 0))
            phot_pattern.append((p*bw, 0))
            phot_pattern.append((1, 1))
            phot_pattern.append((las_period - 2 - p*bw, 0))
        p = p + 1
    return phot_pattern, las_pattern, pix_pattern


def main(pulsestreamer_ip='192.168.178.128'):
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

    # parameters for pattern generation
    tau_base = 200 # ns
    laser_period = 1000 # ns
    pixel_period = 1000000 # ns
    pixels = 100

    # create a sequence-object
    sequence = ps.createSequence()

    # generate and assign the seeding patterns to the digital outputs of PS
    photon = [(1, 0)]
    laser = [(1, 0)]
    pixel = [(1, 0)]
    sync = [(1, 1)]
    sequence.setDigital(1, photon)
    sequence.setDigital(2, laser)
    sequence.setDigital(3, pixel)
    sequence.setDigital(4, sync)

    # generate different patterns for each pixel
    for pix in range(pixels):
        # create a sequence-object
        new_sequence = ps.createSequence()
        # generate next FLIM patterns for PS
        pl_lifetime = tau_base + rnd.randint(0, 300)
        photon, laser, pixel = genFLIM(pl_lifetime, laser_period, pixel_period)
        sync = [(pixel_period + 1, 0)]
        # assign the new patterns to the digital outputs of PS
        new_sequence.setDigital(1, photon)
        new_sequence.setDigital(2, laser)
        new_sequence.setDigital(3, pixel)
        new_sequence.setDigital(4, sync)
        # add the new_sequence to sequence
        sequence = sequence + new_sequence

    # stream the sequence infinitely
    n_runs = PulseStreamer.REPEAT_INFINITELY
    ps.stream(sequence, n_runs)


if __name__ == '__main__':
    main()