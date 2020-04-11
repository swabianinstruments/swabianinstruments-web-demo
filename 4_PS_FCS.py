# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 15:52:30 2020

@author: liu
"""

import random as rnd
from time import sleep

def pattFCS(cells, counts, window, time):
    cell_period = int(window/cells)
    photon_period = int(time/counts)
    pattern = [(0, 0)]
    for c in range(cells):
        rnd_counts = rnd.choice(range(int(0.8*counts), int(1.2*counts)))
        tags = rnd.choices(range(int(0.1*photon_period), int(2*photon_period)), k=rnd_counts)
        for p in range(len(tags)):
            pattern.append((1, 1))
            pattern.append((tags[p], 0))
        skip = rnd.choice(range(int(0.1*cell_period), int(1.5*cell_period)))
        pattern.append((skip, 0))
    return pattern


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

    # create a sequence-object
    sequence = ps.createSequence()

    # parameters for FCS pattern
    n_cells = 100
    em_counts = 1000
    meas_window = 1e9 # in ns, 1s
    pass_time = 1e5 # in ns, 100us

    n_runs = PulseStreamer.REPEAT_INFINITELY
    hold = 1 # second
    # generate new pattern every second and stream
    while True:
        # generate and assign the pattern to a digital output of PS
        patt1 = pattFCS(n_cells, em_counts, meas_window, pass_time)
        sequence.setDigital(1, patt1)
        ps.stream(sequence, n_runs)
        sleep(hold)


if __name__ == '__main__':
    main()