import os
import sys, random
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["figure.figsize"] = [8, 6]
plt.rcParams["figure.autolayout"] = True



def random_bit_message(n_bits):
	
	bit_message = []
	for i in range(0, n_bits):
		bit = random.choice([0,1])
		bit_message.append(bit)
	return bit_message

def setNRZLevels(signal):
	new_sig = []
	for bit in signal:
		if(bit == 0 or bit ==-1.0):
			new_sig.append(-1.0)
		else:
			new_sig.append(1.0) 
	return new_sig

def generate_signal(message, Fs):
	sig = []
	for bit in message:
		for i in range(Fs):
			sig.append(bit)
		pass
	print("Original data:")
	print(message)
	print("Data sampled at "+str(Fs)+" samples/bit. "+ str(len(sig)))
	print(sig)
	return(sig)

def show_signal(signal, title, axs):
	dt = 1/len(signal)
	t = np.arange(0,(len(signal)*dt),dt)

	
	axs.set_title(title)
	axs.plot(t, signal, color='C0')
	axs.set_xlabel("Time")
	axs.set_ylabel("Amplitude")


def spreading_sequence(ss_size, spreading_code_size, ss_sampling_factor):
	ss_code = random_bit_message(spreading_code_size)
	ss = []
	count = 0
	i=0

	print(ss_code)


	while count != ss_size:
		ss.append(ss_code[i])
		count+=1
		i+=1
		if(i==spreading_code_size):
			i=0

	ssg = generate_signal(ss, ss_sampling_factor )
	return ssg 


def product_modulation(signal, spreading_code, spreading_factor):
	i=0
	pm_signal=[]

	for bit in signal: 
		for factor in range(spreading_factor):
			if (len(spreading_code)<=i):
				i=0
			pm_signal.append(bit*spreading_code[i])
			i+=1
			
			

	#print("THIS IS THE PRODUCT OF THE SIGNAL:")
	#print(pm_signal)
	return pm_signal

def file_information(CDMA_signal, message, spreading_code, spreading_factor):
	try:
		path = "C:/Users/jmca-/OneDrive/Ambiente de Trabalho/João Miguel"
		os.chdir(path)

		for file in os.listdir():
    		# Check whether file is in text format or not
    			if file.endswith(".txt"):
        			file_path = f"{path}\{file}"
				
				
		f= open(file_path, "w") 	

		for bit in CDMA_signal:
			f.write("%s;" % str(bit))
		f.write("\n")
		for bit in message:
			f.write("%s;" % str(bit))
		f.write("\n")
		for bit in spreading_code:
			f.write("%s;" % str(bit))
		f.write("\n")
		f.write(str(spreading_factor))
		f.write("\n")
	finally:
		f.close()

#RECEIVER

def get_information(file):
	with open("info.txt", "r") as f: 
		lines = f.read().splitlines()

def interpret_line(line):
	
	for element in line:
		element = element.strip(";")


if __name__ == "__main__":
	n_bits = int(sys.argv[1])
	Fs = int(sys.argv[2])
	spreading_factor = int(sys.argv[3])
	sc_size = int(sys.argv[4])

	fig,(ax1,ax2,ax3) = plt.subplots(3)

	ss_code = random_bit_message(sc_size)
	print(ss_code)
	ss_fs = Fs*spreading_factor
	ss_size = n_bits*spreading_factor

	message = random_bit_message(n_bits)
	signal = generate_signal(message, Fs)
	sig_limited = np.array(setNRZLevels(signal))
	# ss = spreading_sequence(ss_size, sc_size, ss_fs)
	# ss_limited = np.array(setNRZLevels(ss))
	
	output = product_modulation(setNRZLevels(signal),setNRZLevels(ss_code), spreading_factor)
	#print("OUTPUT")
	#print(output)

	file_information(output, signal, ss_code, spreading_factor)

	received = product_modulation(setNRZLevels(output), setNRZLevels(ss_code),1)

	show_signal(sig_limited, "Original Signal",ax1)
	#show_signal(ss_limited, "Spreading Sequence")
	show_signal(output, "Final output",ax2)
	show_signal(received, "Received signal",ax3)

	plt.show() 