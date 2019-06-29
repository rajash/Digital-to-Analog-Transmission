import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from waveform import Waveform
from message import Message
from awgn import Noise

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
        self.waveform = Waveform(self.signal_power, self.carrier_frequency, self.time).cos()
        
    def modulate(self, msg):
        return self.waveform * msg
        
    def demodulate(self, msg_ask):
        msg = list()
        div = msg_ask / self.waveform
        for i in range(0,len(msg_ask),self.sampling_rate):
            if(np.round(np.mean(np.abs(div[i:i+self.sampling_rate]))) == 0):
                msg.append(0)
            elif(np.round(np.mean(np.abs(div[i:i+self.sampling_rate]))) == 1):
                msg.append(1)
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

    # Noisy Channel
    Eb_No = 6        # in Energy per bit to Noise Density
    Noise = Noise(data_rate, Eb_No)
    transmitted_sig = ask.modulate(msg_sampled)
    noise_sig = Noise.data(len(msg_sampled))
    channel_effect = transmitted_sig + noise_sig  
    recieved_sig = ask.demodulate(channel_effect)
    recieved_msg = Message().toText(recieved_sig)

    fig, ax = plt.subplots(3,1,figsize = (20,40))
    ax[0].plot(ask.time, transmitted_sig)
    ax[0].set_ylabel('Transmitted Signal')

    ax[1].plot(ask.time, noise_sig)
    ax[1].set_ylabel('Noise Signal')

    ax[2].plot(ask.time, channel_effect)
    ax[2].set_ylabel('Recieved Signal') 
    ax[2].set_xlabel('Time')

    plt.show()

    print('Sent: ', msg,'\nRecieved: ', recieved_msg)
