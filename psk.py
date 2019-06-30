import numpy as np
import matplotlib.pyplot as plt
from waveform import Waveform
from message import Message

class PSK:
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
        self.waveform1 = Waveform(self.amplitude, self.carrier_frequency, 
                                   self.time
                                  ).cos()
        self.waveform2 = Waveform(self.amplitude, self.carrier_frequency, 
                                   self.time,
                                   np.pi
                                  ).cos()

        
    def modulate(self, msg):
        msg_psk = np.zeros(len(msg))
        
        for i in range(0,len(msg),self.sampling_rate):
            if(np.array_equal(msg[i:i+self.sampling_rate],np.zeros(self.sampling_rate))):
                msg_psk[i:i+self.sampling_rate] = self.waveform1[i:i+self.sampling_rate]
                
            elif(np.array_equal(msg[i:i+self.sampling_rate],np.ones(self.sampling_rate))):
                msg_psk[i:i+self.sampling_rate] = self.waveform2[i:i+self.sampling_rate]

        return msg_psk
    
    def demodulate(self, msg_psk):
        msg = np.zeros((len(msg_psk)//self.sampling_rate)).astype(int)
        
        for i in range(0,len(msg_psk),self.sampling_rate):
            if(np.round(np.mean(np.round(np.abs(msg_psk[i:i+self.sampling_rate] - self.waveform1[i:i+self.sampling_rate])))/self.amplitude) == 0):
                msg[i//self.sampling_rate] = 0
                
            elif(np.round(np.mean(np.round(np.abs(msg_psk[i:i+self.sampling_rate] - self.waveform2[i:i+self.sampling_rate])))/self.amplitude) == 0):
                msg[i//self.sampling_rate] = 1
                
        return np.array(msg)

if __name__ == '__main__':
    data_rate = 1000    # in bps
    sampling_rate = 30  # in samples per bit
    carrier_frequency = 2000    # in Hz
    carrier_space = 1000 # in Hz
    Eb = 1              # energy per bit in joules  

    msg = 'RAJA'
    msg_binary = Message().binary(msg)
    msg_sampled = Message().sample(msg_binary, sampling_rate)

    psk = PSK(data_rate, sampling_rate, carrier_frequency, len(msg_sampled), Eb)

    plt.style.use('ggplot')
    fig, ax = plt.subplots(4,1,figsize = (20,40))
    
    ax[0].plot(psk.time, msg_sampled)
    ax[0].set_ylabel('Message')

    ax[1].plot(psk.time, psk.waveform1)
    ax[1].set_ylabel('Waveform 1')

    ax[2].plot(psk.time, psk.waveform2)
    ax[2].set_ylabel('Waveform 2')

    ax[3].plot(psk.time, psk.modulate(msg_sampled))
    ax[3].set_ylabel('PSK Modulation') 
    ax[3].set_xlabel('Time')

    plt.show()

    demodulate = psk.demodulate(psk.modulate(msg_sampled))
    print('Recieved Demodulated Signal:',
          ' In Binary (', demodulate,
          '), Text (', Message().toText(demodulate),').')

    