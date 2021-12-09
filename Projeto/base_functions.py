import os,sys
import matplotlib.pyplot as plt
import numpy as np
from numpy.core.fromnumeric import size
from numpy.random import default_rng

rng = default_rng()
plt.rcParams["figure.figsize"] = [8, 6]
plt.rcParams["figure.autolayout"] = True



def random_bit_message(n_bits):
	
	bit_message = []
	for i in range(0, n_bits):
		bit = rng.choice([0,1])
		bit_message.append(bit)
	return bit_message

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
	print("DIF= ",(dif/len(output))*100)
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


if __name__ == "__main__":
	

	############ CHANNEL ###############
	print("OUPTUT %s" % output)
	cdma_sig = get_information("transmited.txt", 0)
	at_cdma_sig = add_atenuation(cdma_sig)
	final_sig = add_whitenoise(at_cdma_sig, 0.0)
	channel_sig = []
	for bit in final_sig:
		channel_sig.append("{:.2f}".format(bit))
	file_information("channel.txt",channel_sig, message, ss_code, spreading_factor)

	########### RECEIVER ###############
	



	#received = product_modulation(setNRZLevels(output), setNRZLevels(ss_code),1)

	show_signal(sig_limited, "Original Signal",ax1)
	show_signal(output, "Transmited Signal",ax2)
	show_signal(recv_cdma, "Received Signal",ax3)
	show_signal(recv_message, "Final received message", ax4)

	plt.show() 