import os,sys
import matplotlib.pyplot as plt
import numpy as np
import math
from numpy.core.fromnumeric import size
from numpy.random import default_rng
from sympy import fwht
from sp.gold import gold

rng = default_rng()
plt.rcParams["figure.figsize"] = [8, 6]
plt.rcParams["figure.autolayout"] = True
preferred_pairs = {5:[[2],[1,2,3]], 6:[[5],[1,4,5]], 7:[[4],[4,5,6]],
                        8:[[1,2,3,6,7],[1,2,7]], 9:[[5],[3,5,6]], 
                        10:[[2,5,9],[3,4,6,8,9]], 11:[[9],[3,6,9]]}




def random_bit_message(n_bits):
	
	bit_message = []
	for i in range(0, n_bits):
		bit = rng.choice([0,1])
		bit_message.append(bit)
	return bit_message

def get_walsh_codes(number_of_users):
	walsh_order = int(math.ceil(math.log(number_of_users,2)+float(0.01)))
	wcodes = walsh(walsh_order)
	not_code = [0]*len(wcodes)
	w_codes = wcodes.tolist()
	w_codes.remove(not_code)
	return w_codes

def walsh(order):
    #basic element(order) of walsh code generator
    W = np.array([0])
    for i in range(order):
        W = np.tile(W, (2, 2))
        half = 2**i
        W[half:, half:] = np.logical_not(W[half:, half:])
    return W

def bool2list(bool):
	pass

def get_gold_codes(number_of_users):
	code_order = int(math.ceil(math.log(number_of_users,2)+float(0.01)))+1
	codes = gold(5)
	a_codes = np.array(codes)
	u_codes = (a_codes.astype(int)).tolist()
	print(len(u_codes))
	print(len(u_codes[0]))

	not_code = [0]*len(codes[0])
	try:
		u_codes.remove(not_code)
	except:
		pass
	return u_codes 

#----------------> Gold Codes from http://mubeta06.github.io/python/sp/

# def lfsr(taps, buf):
#     """Function implements a linear feedback shift register
#     taps:   List of Polynomial exponents for non-zero terms other than 1 and n
#     buf:    List of buffer initialisation values as 1's and 0's or booleans
#     """
#     nbits = len(buf)
#     sr = numpy.array(buf, dtype='bool')
#     out = []
#     for i in range((2**nbits)-1):
#         feedback = sr[0]
#         out.append(feedback)
#         for t in taps:
#             feedback ^= sr[t]
#         sr = numpy.roll(sr, -1)
#         sr[-1] = feedback
#     return out

# def gold(n):
#     """Generate a set of 2^n +1 Gold Codes
#     """
#     n = int(n)
#     if not n in preferred_pairs:
#         print('preferred pairs for %s bits unknown' % str(n)) 
#     seed = list(np.ones(n))
#     seq1 = lfsr(preferred_pairs[n][0], seed)
#     seq2 = lfsr(preferred_pairs[n][1], seed)
#     gold = [seq1, seq2]
#     for shift in range(len(seq1)):
#         gold.append(numpy.logical_xor(seq1, numpy.roll(seq2, -shift)))
#     return gold

#--------------------------------------------------------------------------
	
def setNRZLevels(signal):
	new_sig = []
	for bit in signal:
		if(bit == 0 or bit ==-1):
			new_sig.append(-1)
		else:
			new_sig.append(1) 
	return new_sig

def generate_signal(message, Fs):
	sig = []
	for bit in message:
		for i in range(Fs):
			sig.append(bit)
		pass
	# print("Original data:")
	# print(message)
	# print("Data sampled at "+str(Fs)+" samples/bit. "+ str(len(sig)))
	# print(sig)
	return(sig)

def show_signal(signal, title, axs):
	dt = 1/len(signal)
	t = np.arange(0,(len(signal)*dt),dt)

	
	axs.set_title(title)
	axs.plot(t, signal, color='C0')
	axs.set_xlabel("Time")
	axs.set_ylabel("Amplitude")


def spreading_sequence(ss_size, spreading_code, ss_sampling_factor):
	ss = []
	count = 0
	i=0

	
	while count != ss_size:
		ss.append(spreading_code[i])
		count+=1
		i+=1
		if(i==len(spreading_code)):
			i=0
	ssg = generate_signal(ss, ss_sampling_factor )
	return ssg 


def product_modulation(signal, spreading_code, spreading_factor, chip_rate):
	i=0
	pm_signal=[]

	for bit in signal: 
		for factor in range(spreading_factor):
			if (len(spreading_code)<=i):
				i=0
			for chip in range(chip_rate):
				pm_signal.append(bit*spreading_code[i])
			i+=1
	return pm_signal

def product_modulation_r(signal, spreading_sequence):

	result_sig=[]
	for idx in range(len(signal)):
		result_sig.append(signal[idx]*spreading_sequence[idx])
	return result_sig			

	#print("THIS IS THE PRODUCT OF THE SIGNAL:")
	#print(pm_signal)
	return pm_signal

def file_information(file, writing_mode, CDMA_signal, message, spreading_code, spreading_factor):
		# path = ""
		# os.chdir(path)

		# for file in os.listdir():
  #   		# Check whether file is in text format or not
  #   			if file.endswith(".txt"):
  #       			file_path = f"{path}\{file}"
				

		with open(file, writing_mode) as f:
			if CDMA_signal != None:
				for bit in CDMA_signal[:-1]:
					f.write("%s," % str(bit))
				f.write("%s\n" % str(CDMA_signal[-1]))
			for bit in message[:-1]:
				f.write("%s," % str(bit))
			f.write("%s\n" % str(message[-1]))
			for bit in spreading_code[:-1]:
				f.write("%s," % str(bit))
			f.write("%s\n" % str(spreading_code[-1]))
			f.write(str(spreading_factor))
			f.write("\n")

#CHANNEL

def add_atenuation(signal, atenuation_level):
	attenuation_factor = rng.uniform(1-atenuation_level,1)
	res = []
	for bit in signal:
		res.append(bit * attenuation_factor)
	return res

def add_whitenoise(signal, noise_deviation):

	res = []
	for bit in signal:
		normal = rng.normal(0, noise_deviation)
		
		res.append(bit+normal)
	#print('NOISE %s' % res)
	return res




#RECEIVER

def get_information(file, index):
	res = []
	with open(file, "r") as f: 
		lines = f.read().splitlines()
	line = lines[index].split(',')
	for bit in line:
		if index == 0 :
			res.append(float(bit))
		elif index == 3:
			res.append(bit)
		else:
			res.append(int(bit)) 

	return res


#BER

def signal_comp(output, recv_message):
	dif = 0
	for bit in range(len(output)):
		if output[bit] != recv_message[bit]:
			dif = dif + 1

	print(dif)
	print(len(output))
	return dif/len(output)			


def integrate_signal(signal, Fs):
	result_sig=[]
	res = 0
	i=1
	for bit in signal:
		if i != Fs:
			res += bit
			i+=1
		else:
			i=1
			res = res/Fs
			if res < 0:
				result_sig.append(0)
			else:
				result_sig.append(1)
	return result_sig

