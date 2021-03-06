# Burak Bozdag
# 150170110

import numpy as np # Fundamental operations
import matplotlib.pyplot as plt # Plotting
import sys # Arguments
from scipy.io.wavfile import read as readWav # Reading wave files

windowMs = (256.0 / 44100.0) * 1000.0 # Window size for 256-point

def spectrogram(samples, sample_rate, stride_ms = windowMs / 2,
                window_ms = windowMs, max_freq = 22050, eps = 1e-14):
    stride_size = int(0.001 * sample_rate * stride_ms)
    window_size = int(0.001 * sample_rate * window_ms)

    truncate_size = (len(samples) - window_size) % stride_size
    samples = samples[:len(samples) - truncate_size]
    nshape = (window_size, (len(samples) - window_size) // stride_size + 1)
    nstrides = (samples.strides[0], samples.strides[0] * stride_size)
    windows = np.lib.stride_tricks.as_strided(samples, shape = nshape, strides = nstrides)

    assert np.all(windows[:, 1] == samples[stride_size:(stride_size + window_size)])

    weighting = np.hanning(window_size)[:, None]

    fft = np.fft.rfft(windows * weighting, axis = 0)
    fft = np.absolute(fft)
    fft = fft ** 2

    scale = np.sum(weighting ** 2) * sample_rate
    fft[1:-1, :] *= (2.0 / scale)
    fft[(0, -1), :] /= scale

    freqs = float(sample_rate) / window_size * np.arange(fft.shape[0])

    ind = np.where(freqs <= max_freq)[0][-1] + 1
    spectogram = np.log(fft[:ind, :] + eps)
    return spectogram

rate, audData = readWav(sys.argv[1])

lenData = len(audData)

channel1 = np.zeros(2 ** (int(np.ceil(np.log2(lenData)))))
channel1[0:lenData] = audData

fourier = np.fft.fft(channel1)
w = np.linspace(0, 44100, len(fourier))

fourierToPlot = fourier[0:len(fourier) // 2]
w = w[0:len(fourier) // 2]

print("Calculating convolution 1...")
convolved1 = np.convolve(audData[44100*10:44100*11], fourierToPlot[44100*10:44100*11])
print("Calculation completed.")

print("Calculating convolution 2...")
convolved2 = np.convolve(audData[44100*20:44100*21], fourierToPlot[44100*20:44100*21])
print("Calculation completed.")

print("Calculating convolution 3...")
convolved3 = np.convolve(audData[44100*30:44100*31], fourierToPlot[44100*30:44100*31])
print("Calculation completed.")

fig, (ax1, ax2, ax3) = plt.subplots(3)
fig.suptitle("Graphs")

ax1.plot(w[44100*10:(44100*12)-1], convolved1)

ax2.plot(w[44100*20:(44100*22)-1], convolved2)

ax3.plot(w[44100*30:(44100*32)-1], convolved3)

plt.show()

