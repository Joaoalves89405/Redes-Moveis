import sys,random
import matplotlib.pyplot as plt
import numpy as np
import bitarray.util as ba

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True



def random_bit_message(n_bits):
	
	bit_message = ba.urandom(n_bits)
	return bit_message

def setSigLevels(signal):
	new_sig = []
	for bit in signal:
		if(bit == 0):
			new_sig.append(-1)
		else:
			new_sig.append(bit) 
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

def show_signal(signal, title):
	dt = 1/len(signal)
	t = np.arange(0,(len(signal)*dt),dt)

	fig, axs = plt.subplots()
	axs.set_title(title)
	axs.plot(t, signal, color='C0')
	axs.set_xlabel("Time")
	axs.set_ylabel("Amplitude")


def spreading_sequence(ss_size, spreading_code_size, ss_sampling_factor):
	ss_code = random_bit_message(spreading_code_size)
	ss = [ss_size]
	count = 0
	i=1

	while count != ss_size:
		ss.append(ss_code[i])
		count+=1
		i+=1
		if(i==spreading_code_size):
			i=0

	ssg = generate_signal(ss, ss_sampling_factor )
	return ssg 


if __name__ == "__main__":
	n_bits = int(sys.argv[1])
	Fs = int(sys.argv[2])
	spreading_factor = int(sys.argv[3])
	sc_size = int(sys.argv[4])



	ss_fs = Fs*spreading_factor
	ss_size = n_bits*spreading_factor

	message = random_bit_message(n_bits)
	signal = np.array(generate_signal(message, Fs))
	sig_limited = setSigLevels(signal)
	ss = np.array(spreading_sequence(ss_size, sc_size, ss_fs))
	ss_limited = setSigLevels(ss)
	
	#output = signal*ss


	show_signal(sig_limited, "Original Signal")
	show_signal(ss, "Spreading Sequence")
	#show_signal(output, "Final output")

	plt.show()