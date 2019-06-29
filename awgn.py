import numpy as np
import matplotlib.pyplot as plt

class Noise:
    def __init__(self, data_rate, Eb_No):
        self.data_rate = data_rate
        self.Eb_No = (10**(Eb_No/10))        
        self.SNR = data_rate * self.Eb_No
        
    def data(self, no_samples):
        return  np.random.normal(0, np.sqrt(self.SNR), no_samples)

if __name__ == '__main__':
    data_rate = 1000 # in bps
    Eb_No = 6        # in Energy per bit to Noise Density
    num_samples = 100 # number of data points to generate
    Noise = Noise(data_rate, Eb_No)

    plt.style.use('ggplot')
    plt.plot(range(num_samples), Noise.data(num_samples))
    plt.show()

    