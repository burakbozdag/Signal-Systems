import numpy as np
import wave
import math
import contextlib

cutOffFreq = 2000.0 # fc = 2000Hz

# Low pass filter
def l_filter(x, window_size):
   cumSum = np.cumsum(np.insert(x, 0, 0))
   return (cumSum[window_size:] - cumSum[:-window_size]) / window_size

def interpret_wav(raw_bytes, n_frames, n_channels, sample_width):
    # Bit format checking
    if sample_width == 1:
        dtype = np.uint8 # 8-bit
    elif sample_width == 2:
        dtype = np.int16 # 16-bit
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")

    channels = np.fromstring(raw_bytes, dtype=dtype)

    # Interleaved channels
    channels.shape = (n_frames, n_channels)
    channels = channels.T

    return channels

def pass_filter(name):
    with contextlib.closing(wave.open(name + ".wav",'rb')) as spf:
        sampleRate = spf.getframerate() # Sampling rate = 44100Hz
        nChannels = spf.getnchannels()
        nFrames = spf.getnframes()
        sampWidth = spf.getsampwidth() # 1 or 2 bytes are allowed (8-16 bit audios)

        signal = spf.readframes(nFrames * nChannels) # Extracting audio from wav file
        spf.close()
        channels = interpret_wav(signal, nFrames, nChannels, sampWidth) # Channel separation

        freqRatio = (cutOffFreq / sampleRate)
        N = int(math.sqrt(0.196196 + freqRatio ** 2) / freqRatio) # Constant math formula for window length

        filtered = l_filter(channels[0], N).astype(channels.dtype) # Applying LPF

        wav_file = wave.open(name + "LPF.wav", "w")
        wav_file.setparams((1, sampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
        wav_file.writeframes(filtered.tobytes('C'))
        wav_file.close()

        for i in range(0, len(filtered)): # Subtracting filtered audio from the original audio
            channels[0][i] -= filtered[i]

        # channels[0] is now HPF of the original audio
        wav_file = wave.open(name + "HPF.wav", "w")
        wav_file.setparams((1, sampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
        wav_file.writeframes(channels[0].tobytes('C'))
        wav_file.close()

name = "Africa"
pass_filter(name)

name = "WinnerTakesAll"
pass_filter(name)