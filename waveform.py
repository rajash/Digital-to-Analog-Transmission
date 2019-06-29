import numpy as np
import matplotlib.pyplot as plt

class Waveform:
    def __init__(self, signal_power, freq, t, phase = 0):
        self.frequency = freq
        self.time = t
        self.phase = phase
        self.signal_power = signal_power
        
    def sin(self,):
        return self.signal_power * np.sin((2 * np.pi * self.frequency * self.time) + self.phase)
    
    def cos(self,):
        return self.signal_power * np.cos((2 * np.pi * self.frequency * self.time) + self.phase)    

if __name__ == '__main__':
    signal_power = 1 # in Watt
    frequency = 2000        # in Hz
    time = np.arange(0,1,0.01) # time range (1s)
    phase = np.pi/4              # starting position (angle)
    Waveform = Waveform(signal_power, frequency, time, phase)

    plt.style.use('ggplot')
    fig, ax = plt.subplots(2,1,figsize = (40,20))
    
    ax[0].plot(time, Waveform.sin())
    ax[0].set_title('Sine Wave')
    ax[0].set_ylabel('Amplitude')

    ax[1].plot(time, Waveform.cos())
    ax[1].set_title('Cosine Wave')
    ax[1].set_xlabel('Time')
    ax[1].set_ylabel('Amplitude')
    plt.show()