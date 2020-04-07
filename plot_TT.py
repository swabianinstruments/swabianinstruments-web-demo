# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:55:35 2020

@author: liudm
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.optimize import curve_fit

def exponent(t, A, tau):
    return (A * np.exp(- t / tau) )

# Plot the TRPL curve
def ScatterPlot(x, y):
    xlim = np.max(x)
    ylim = np.max(y)
    plt.figure('ScatterPlot', [4,3], 200)
    plt.scatter(x/1e6, y, color=(31/255, 162/255, 213/255), s=5, alpha=0.5)
    plt.tick_params('x', labelsize=10, bottom=True, top=True, direction='in', length=4)
    plt.tick_params('y', labelsize=10, left=True, right=True, direction='in', length=4)
    plt.xlabel('Time (µs)', fontsize=12)
    plt.ylabel('Counts', fontsize=12)
    plt.xlim(0, 1.01*xlim/1e6)
    plt.ylim(0.0, 1.01*ylim)
    plt.title("Start-Stop Histogram")
    plt.show()
    
        
# Plot the TRPL curve
def ScatterLogPlot(x, y):
    xlim = np.max(x)
    ylim = np.max(y)
    plt.figure('ScatterLogPlot', [4,3], 200)
    plt.scatter(x/1e6, y/ylim, color=(31/255, 162/255, 213/255), s=5, alpha=0.5)
    plt.tick_params('x', labelsize=10, bottom=True, top=True, direction='in', length=4)
    plt.tick_params('y', labelsize=10, left=True, right=True, direction='in', length=4)
    plt.xlabel('Time (µs)', fontsize=12)
    plt.ylabel('Counts (norm.)', fontsize=12)
    plt.yscale("log")
    plt.xlim(0, 1.01*xlim/1e6)
    plt.ylim(0.01, 1.1)
    plt.title("Start-Stop Histogram")
    plt.show()

def LinePlot(x, y):
    xlim = np.max(x)
    ylim = np.max(y)
    plt.figure('LinePlot', [4,3], 200)
    plt.plot(x/1e6, y, color=(0/255, 92/255, 148/255), linewidth=1)
    plt.tick_params('x', labelsize=10, bottom=True, top=True, direction='in', length=4)
    plt.tick_params('y', labelsize=10, left=True, right=True, direction='in', length=4)
    plt.xlabel('Time (µs)', fontsize=12)
    plt.ylabel('Counts', fontsize=12)
    plt.xlim(-1.01*xlim/1e6, 1.01*xlim/1e6)
    plt.ylim(0.0, 1.01*ylim)
    plt.title("Correlation")
    plt.show()
    
def ScatterLogBinsPlot(bins, y, lf, rg):
    xlim = bins[-1]
    x = np.delete(bins, -1)
    ylim = np.max(y)
    plt.figure('ScatterLogBinsPlot', [4,3], 200)
    plt.scatter(x/1e12, y, color=(255/255, 150/255, 40/255), s=20)
    plt.tick_params('x', labelsize=10, bottom=True, top=False, direction='out', length=4)
    plt.tick_params('y', labelsize=10, left=True, right=False, direction='out', length=4)
    plt.xlabel('Time (s)', fontsize=12)
    plt.ylabel('Counts (g2-norm.)', fontsize=12)
    plt.xscale('log')
    #plt.yscale('log')
    plt.xlim(10**lf, 10**rg)
    plt.ylim(0, 1.1*ylim)
    plt.title("Start-Stop Histogram with Log Bins")
    plt.show()
    
# Plot the TRPL curve
def BarChart(x, y):
    xlim = np.max(x)
    ylim = np.max(y)
    plt.figure('BarChart', [4,3], 200)
    plt.bar(x/1e3, y, color=(31/255, 162/255, 213/255), edgecolor='black')
    plt.tick_params('x', labelsize=10, bottom=True, top=True, direction='in', length=4)
    plt.tick_params('y', labelsize=10, left=True, right=True, direction='in', length=4)
    plt.xlabel('Time (ns)', fontsize=12)
    plt.ylabel('Counts', fontsize=12)
    plt.xlim(0, 1.01*xlim/1e3)
    plt.ylim(0.0, 1.01*ylim)
    plt.title("Start-Stop Histogram")
    plt.show()
    
def BarChart2D(x, y):
    x_pix = int(np.sqrt(len(y)))
    lifetimes = np.zeros((x_pix, x_pix))
    for i in range(len(y)):
        peak = np.max(y[i])
        half = peak/2
        q = 0
        while ((y[i, q] > half) and (q < len(y[i])-1)):
            q = q + 1
        half_life = x[q]
        init_values = [peak, half_life/0.69]
        optim_values = curve_fit(exponent, x, y[i], init_values)
        A = optim_values[0][0]
        tau = optim_values[0][1]
        lifetimes[int(i/x_pix)][int(i%x_pix)] = int(tau/1e3)
        yExpFit = np.zeros(x.size)
        for g in range(x.size):
            yExpFit[g] = exponent(x[g], A, tau)
        plt.figure('BarChart2D'+str(i), [4,3], 170)
        rgb = cm.get_cmap('winter_r')((tau/1e3-200)/300)[:3]
        plt.bar(x/1e3, y[i], color=rgb, width=0.8*(x[1]-x[0])/1e3)
        plt.plot(x/1e3, yExpFit, color='gray', linewidth=0.8)
        plt.tick_params('x', labelsize=10, bottom=True, top=True, direction='in', length=4)
        plt.tick_params('y', labelsize=10, left=True, right=True, direction='in', length=4)
        plt.xlabel('Time (ns)', fontsize=12)
        plt.ylabel('Counts', fontsize=12)
        plt.title('Pixel '+str(i+1))
        plt.annotate('Lifetime: '+str(int(tau/1e3))+' ns', (0.55*x[-1]/1e3, 0.6*peak))
        plt.show()
    plt.figure('FLIM', [4,4], 230)
    plt.pcolormesh(np.linspace(0.5, x_pix+0.5, 11), np.linspace(0.5, x_pix+0.5, 11), lifetimes, vmin=200, vmax=500, cmap='winter_r')
    plt.xlim(0.5, x_pix+0.5)
    plt.ylim(0.5, x_pix+0.5)
    plt.xticks(np.linspace(1, x_pix, x_pix))
    plt.yticks(np.linspace(1, x_pix, x_pix))
    plt.tick_params('x', labelsize=7, bottom=True, top=True, direction='out', length=2)
    plt.tick_params('y', labelsize=7, left=True, right=True, direction='out', length=2)
    plt.title('Fluorescence Lifetime (ns)')
    for i in range (x_pix):
        for j in range (x_pix):
            plt.text(i+1, j+1, int(lifetimes[j,i]), ha='center', va='center', color='white', fontsize=6)
    plt.show()
    

    
