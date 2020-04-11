from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from TimeTagger import createTimeTagger, freeAllTimeTagger, Correlation

def Gauss(t, G0, t0, sigma):
    return G0 * np.exp(-(t - t0)**2 / 2 / sigma**2)
    
def getFWHM(x, y):
    M = np.max(y)
    base = np.min(y)
    HM = (M - base)/2
    top_index = np.argwhere(y > HM)
    in1 = top_index[0,0]
    in2 = in1 + 1
    x1 = x[in1]
    x2 = x[in2]
    y1 = y[in1]
    y2 = y[in2]
    a = (y2-y1)/(x2-x1)
    k = (y1*x2 - y2*x1)/(x2 - x1)
    xlHM = (HM - k)/a
    in1 = top_index[top_index.size-1,0]
    in2 = in1 + 1
    x1 = x[in1]
    x2 = x[in2]
    y1 = y[in1]
    y2 = y[in2]
    a = (y2-y1)/(x2-x1)
    k = (y1*x2 - y2*x1)/(x2 - x1)
    xrHM = (HM - k)/a
    FWHM = xrHM - xlHM
    return FWHM
    
def getRMSgen(x, y):
    N = np.sum(y)
    avx = np.sum(x*y)/N
    var = (np.sum(y*(x-avx)**2))/(N-1)
    return np.sqrt(var)

# create a Time Tagger instance
tagger = createTimeTagger()
tagger.reset()

# sets the channel numbers
nch1 = 1
nch2 = 2

# disable the normalization
#tagger.setNormalization(False)

# sets the test signal on the designated channels
tagger.setTestSignal([nch1, nch2], True)
tagger.sync()

# calculates and sets an optimal delay at the first channel to center the correlation curve
corr = Correlation(tagger, nch1, nch2, binwidth=int(10), n_bins=5000)
print("\nCorrelation measurement is running.")
sleep(2.0)
xcorr = corr.getIndex()
ycorr = corr.getData()
corr.clear()
delay = int(xcorr[ycorr.argmax()])
tagger.setInputDelay(nch1,-delay)

# parameters for plotting
bins = 1000
jtt0 = 10
plt_title = 'TTU8: RMS Jitter per Channel (ps)'

# Calculates correlation between channels 1 and 2
corr = Correlation(tagger, nch1, nch2, binwidth=int(1), n_bins=bins)
sleep(5.0)
xcorr = corr.getIndex()
ycorr = corr.getData()
M = np.max(ycorr)

# terminate the open connection to the Time Tagger
freeAllTimeTagger()

# Calculates FWHM of the correlation peak
FWHM = getFWHM(xcorr, ycorr)

# Calculates RMS jitter by generic formula through the square root of variation
RMSgen = getRMSgen(xcorr, ycorr)

# Gaussian fit of the correlation data
init_values = [1, xcorr[ycorr.argmax()], FWHM/2.35]
optim_values = curve_fit(Gauss, xcorr, ycorr/M, init_values)
G0 = optim_values[0][0]
t0 = optim_values[0][1]
sigma = abs(optim_values[0][2])

# Calculates RMS jitter per channel from the Gaussian fit
RMS = round(sigma/np.sqrt(2), 1)

# Creating the corresponding Gaussian curve for plotting
yGaussFit = np.zeros(xcorr.size)
for g in range(xcorr.size-1):
    yGaussFit[g] = Gauss(xcorr[g], G0, t0, sigma)

# Plot the correlation peak
plt.figure('corr', [4,3], 200)
plt.plot(xcorr, ycorr/M, color='cyan', linewidth=3)
plt.plot(xcorr, yGaussFit, color='black', linewidth=1, linestyle='--')
plt.tick_params('x', labelsize=10, bottom=True, top=True, direction='in', length=4)
plt.tick_params('y', labelsize=10, left=True, right=True, direction='in', length=4)
plt.xlabel('Time (ps)', fontsize=12)
plt.ylabel('Counts (norm.)', fontsize=12)
plt.xlim(t0-2*FWHM,t0+2*FWHM)
plt.ylim(0.0,1.2)
plt.title("Correlation between channels 1 and 2")
plt.show()

# Calculates and prints the jitter parameters
print('Time resolution per channel:')
print('FWHM/Sqrt(2) = ', round(FWHM/np.sqrt(2), 1), ' ps')
print('Sigma/Sqrt(2): ', RMS, ' ps')