# web-demo
Demo scripts for Time Tagger and Pulse Streamer.

Connect  four digital channels of Pulse Streamer to Time Tagger inputs:
1 PS -> 1 TT
2 PS -> 2 TT
3 PS -> 3 TT
4 PS -> 4 TT

First, run a PS script in python.
Then, run the corresponding TT script in python or show the result in TT web-interface.
Parameters are such that one can use Time Tagger 20 as well as Time Tagger Ultra 8. 
All TT scripts use file "plot_TT.py". Make sure it is in the folder.

Description:

1. TRPL and Antibunching.
Shows that two different measurements can run in parallel
(Time-resolved photoluminescence as histogram and antibunching as correlation).

2. TRPL_high pulsing rate.
Shows conditional filter for 80 MHz repetition rate.

3. FLIM
Uses TimeDifferences measurement class to imitate 2D historgam measurements.

4. FCS
Imitates FCS measurement to demonstrate logarithmic time binning.
