import numpy as np
import matplotlib.pyplot as plt
import random
from waveform import Waveform
from message import Message
from awgn import Noise

class FSK:
    def __init__(self, DR, SR, Fc, Cs, msg_len, Eb):
        self.data_rate = DR 
        self.sampling_rate = SR
        self.sampling_frequency = SR*DR;  # samples per sec
        self.sampling_interval = 1.0 / self.sampling_frequency;  
        self.carrier_frequency = Fc # (Hz)
        self.carrier_space = Cs # carrier space (Hz)
        self.time = np.arange(0, self.sampling_interval*msg_len, self.sampling_interval)  # time space
        self.bit_energy = Eb
        self.signal_power =  DR * Eb
        self.waveform1 = Waveform(self.signal_power,
                               self.carrier_frequency - (self.carrier_space / 2), 
                               self.time
                              ).sin()
        self.waveform2 = Waveform(self.signal_power,
                               self.carrier_frequency + (self.carrier_space / 2), 
                               self.time
                              ).sin()
        
    def modulate(self, msg):
        msg_fsk = np.zeros(len(msg))
        
        for i in range(0,len(msg),self.sampling_rate):
            if(np.array_equal(msg[i:i+self.sampling_rate],np.zeros(self.sampling_rate))):
                msg_fsk[i:i+self.sampling_rate] = self.waveform1[i:i+self.sampling_rate]
                
            elif(np.array_equal(msg[i:i+self.sampling_rate],np.ones(self.sampling_rate))):
                msg_fsk[i:i+self.sampling_rate] = self.waveform2[i:i+self.sampling_rate]
                
        return msg_fsk
    
    def demodulate(self, msg_fsk):
        msg = list()
        
        for i in range(0,len(msg_fsk),self.sampling_rate):

            if(np.round(np.mean(np.round(np.abs(msg_fsk[i:i+fsk.sampling_rate] - self.waveform1[i:i+fsk.sampling_rate])))/self.signal_power) == 0):
                msg.append(0)
                
            elif(np.round(np.mean(np.round(np.abs(msg_fsk[i:i+fsk.sampling_rate] - self.waveform2[i:i+fsk.sampling_rate])))/self.signal_power) == 0):
                msg.append(1)

        return np.array(msg)

if __name__ == '__main__':
    data_rate = 1000    # in bps
    sampling_rate = 30  # in samples per bit
    carrier_frequency = 2000    # in Hz
    carrier_space = 1000 # in Hz
    Eb = 1              # energy per bit in jual  
    msg = 'We are testing the performance of our RECEIVER!'
    msg_binary = Message().binary(msg)
    msg_sampled = Message().sample(msg_binary, sampling_rate)

    fsk = FSK(data_rate, sampling_rate, carrier_frequency, carrier_space, len(msg_sampled), Eb)

    plt.style.use('ggplot')
    fig, ax = plt.subplots(4,1,figsize = (20,40))
    
    ax[0].plot(fsk.time, msg_sampled)
    ax[0].set_ylabel('Message')

    ax[1].plot(fsk.time, fsk.waveform1)
    ax[1].set_ylabel('Waveform 1')

    ax[2].plot(fsk.time, fsk.waveform2)
    ax[2].set_ylabel('Waveform 2')

    ax[3].plot(fsk.time, fsk.modulate(msg_sampled))
    ax[3].set_ylabel('FSK Modulation') 
    ax[3].set_xlabel('Time')

    plt.show()

    demodulate = fsk.demodulate(fsk.modulate(msg_sampled))
    print('Recieved Demodulated Signal:',
          ' In Binary (', demodulate,
          '), Text (', Message().toText(demodulate),').')

    # Noisy Channel
    Eb_No = 6        # in Energy per bit to Noise Density
    num_bits = len(msg_sampled)/30
    Noise = Noise(data_rate, Eb_No)
    transmitted_sig = fsk.modulate(msg_sampled)
    noise_sig = Noise.data(len(msg_sampled))
    channel_effect = transmitted_sig + noise_sig  
    recieved_sig = fsk.demodulate(channel_effect)
    recieved_msg = Message().toText(recieved_sig)
    fig, ax = plt.subplots(3,1,figsize = (20,40))
    ax[0].plot(fsk.time, transmitted_sig)
    ax[0].set_ylabel('Transmitted Signal')

    ax[1].plot(fsk.time, noise_sig)
    ax[1].set_ylabel('Noise Signal')

    ax[2].plot(fsk.time, channel_effect)
    ax[2].set_ylabel('Recieved Signal') 
    ax[2].set_xlabel('Time')

    plt.show()

    print('Sent: ', msg,'\nRecieved: ', recieved_msg)