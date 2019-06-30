import matplotlib.pyplot as plt
import numpy as np
from waveform import Waveform
from message import Message

class ASK:
    def __init__(self, DR, SR, Fc, msg_len, Eb):
        self.data_rate = DR
        self.sampling_rate = SR
        self.sampling_frequency = SR*DR;  # samples per sec
        self.sampling_interval = 1.0 / self.sampling_frequency; 
        self.carrier_frequency = Fc # (Hz)
        self.time = np.arange(0, self.sampling_interval*msg_len, self.sampling_interval)  # time space
        self.bit_energy = Eb
        self.signal_power = DR * Eb
        self.amplitude =  np.sqrt(self.signal_power)
        self.waveform = Waveform(self.amplitude, self.carrier_frequency, self.time).cos()
        
    def modulate(self, msg):
        return self.waveform * msg
        
    def demodulate(self, msg_ask):
        msg = np.zeros((len(msg_ask)//self.sampling_rate)).astype(int)
        div = msg_ask / self.waveform
        for i in range(0,len(msg_ask),self.sampling_rate):
            if(np.round(np.mean(np.abs(div[i:i+self.sampling_rate]))) == 0):
               msg[i//self.sampling_rate] = 0
            elif(np.round(np.mean(np.abs(div[i:i+self.sampling_rate]))) == 1):
                msg[i//self.sampling_rate] = 1
        return np.array(msg)

if __name__ == '__main__':
    data_rate = 1000    # in bps
    sampling_rate = 30  # in samples per bit
    carrier_frequency = 2000    # in Hz
    Eb = 1              # energy per bit in jual  
    msg = 'Hello World!'
    msg_binary = Message().binary(msg)
    msg_sampled = Message().sample(msg_binary, sampling_rate)

    ask = ASK(data_rate, sampling_rate, carrier_frequency, len(msg_sampled), Eb)

    plt.style.use('ggplot')
    fig, ax = plt.subplots(3,1,figsize = (20,40))
    
    ax[0].plot(ask.time, msg_sampled)
    ax[0].set_ylabel('Message')

    ax[1].plot(ask.time, ask.waveform)
    ax[1].set_ylabel('Waveform')

    ax[2].plot(ask.time, ask.modulate(msg_sampled))
    ax[2].set_ylabel('ASK Modulation') 
    ax[2].set_xlabel('Time')

    plt.show()

    demodulate = ask.demodulate(ask.modulate(msg_sampled))
    print('Recieved Demodulated Signal:',
          ' In Binary (', demodulate,
          '), Text (', Message().toText(demodulate),').')
