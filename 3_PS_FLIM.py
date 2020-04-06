# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:19:50 2020

@author: liu
"""

import numpy as np
import random as rnd
from time import sleep

def expPL(tau, binwidth, bins, counts):
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

def genFLIM(pl_lt, las_period, pix_period):
    pix_pattern = [(1, 1), (pix_period, 0)]
    las_pattern = [(1, 0), (1, 1), (las_period - 1, 0)]
    las_counts = int(pix_period/las_period)
    for i in range(1, las_counts):
        las_pattern.append((1, 1))
        las_pattern.append((las_period - 1, 0))
    bw = 10
    bns = 100
    phot_distr = expPL(pl_lt, bw, bns, las_counts)
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

# import API classes into the current namespace
from pulsestreamer import PulseStreamer

# IP of Pulse Streamer connected directly by Ethernet cable
ip = '169.254.8.2'

# connect to the Pulse Streamer
ps = PulseStreamer(ip)

# parameters for pattern generation
tau_base = 270 # ns
laser_period = 1000 # ns
pixel_period = 1000000 # ns
pixels = 10

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
    pl_lifetime = tau_base + 50*np.abs((pixels-1)/2-pix)
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
