# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 15:52:30 2020

@author: liu

"""

NAME = 'FCS'
DESCR = """
This example uses **Pulse Streamer** to emulate signals for fluorescence correlation spectroscopy (FSC).
The example demonstrates autocorrelation measurement with logarithmic binning.

* Channel 1 - fluorescence photons

"""

import random as rnd

def pattFCS(cells, counts, window, time):
    cell_period = int(window/cells-time)
    photon_period = int(time/counts)
    pattern = [(0, 0)]
    for c in range(cells):
        rnd_counts = rnd.randint(int(0.8*counts), int(1.2*counts))
        for i in range(rnd_counts):
            pattern.append((3, 1))
            tag= rnd.randint(3, int(2*photon_period))
            pattern.append((tag, 0))
        skip = rnd.randint(3, int(2*cell_period))
        pattern.append((skip, 0))
    return pattern


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

    # create a sequence-object
    sequence = ps.createSequence()

    # parameters for FCS pattern
    n_cells = 10
    em_counts = 1000
    meas_window = 1e9 # in ns, 1s
    pass_time = 1e5 # in ns, 100us

    # generate new pattern every second and stream
    while True:
        # generate and assign the pattern to a digital output of PS
        patt1 = pattFCS(n_cells, em_counts, meas_window, pass_time)
        sequence.setDigital(1, patt1)
        ps.stream(sequence, 1)


if __name__ == '__main__':
    main()