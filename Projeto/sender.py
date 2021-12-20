import base_functions as bf
import matplotlib.pyplot as plt
import numpy as np
from sympy import fwht

n_bits = 10
chip_rate = 2
spreading_factor = 4
sc_size = 6
		


if __name__ == '__main__':
	
	nr_sinais = int(input("Numero de sinais: "))

	Fs = chip_rate*spreading_factor
	gc = bf.get_walsh_codes(nr_sinais)
	#gc = bf.get_gold_codes(nr_sinais)
	print(gc)


	for users in range(nr_sinais):
		fig,(ax1,ax2) = plt.subplots(2)
		path_file = ("./transmited/transmited"+str(users+1)+".txt")
		ss_code = gc[users]
		message = bf.random_bit_message(n_bits)
		signal = bf.generate_signal(message, Fs)
		sig_limited = np.array(bf.setNRZLevels(signal))
		
		print("Length initial sig", len(signal))
		
		output = bf.product_modulation(bf.setNRZLevels(signal),bf.setNRZLevels(ss_code), spreading_factor, chip_rate)
		#print(output) 
		bf.file_information(path_file, "w", output, signal, ss_code, spreading_factor)
		print("Length output sig", len(output))

		bf.show_signal(sig_limited, "Original Signal",ax1)
		bf.show_signal(output, "Transmited Signal",ax2)
		
		plt.show() 
	# ss_code = bf.random_bit_message(sc_size)
	# print(ss_code)



