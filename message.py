import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class Message:
    def __init__(self,):
        pass
    
    def binary(self, msg):
        binary_msg = ''
        msg = msg.replace('\n',' ')
        for data in msg:
            binary_msg = binary_msg + '{0:0b}'.format(ord(data)).zfill(7)
        return binary_msg
        
    def toText(self,binr):
        if(type(binr)==np.ndarray):
            binr = ''.join([str(b) for b in binr])
        msg_str = ''
        for i in range(0,len(binr),7):
            n = int(binr[i:i+7],2)
            msg_str = msg_str + chr(n)
        return msg_str
    
    def sample(self, data, samples):
        bits = list()
        for d in data:
            bits.append(int(d))
        return np.repeat(np.array(bits), samples)


if __name__ == '__main__':
    msg = 'Hi!'
    msg_sig = Message()
    msg_bin = msg_sig.binary(msg)
    print('Message: ', msg,' To Binary Message: ', msg_bin,
          ' To Text Again: ', msg_sig.toText(msg_bin))


