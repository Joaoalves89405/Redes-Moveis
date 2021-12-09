import base_functions as bf
import matplotlib.pyplot as plt
import numpy as np

n_bits = 20
chip_rate = 2
spreading_factor = 4
sc_size = 4
		



if __name__ == '__main__':
	
	Fs = chip_rate*spreading_factor
	fig,(ax1,ax2) = plt.subplots(2)

	ss_code = bf.random_bit_message(sc_size)
	print(ss_code)

	message = bf.random_bit_message(n_bits)
	signal = bf.generate_signal(message, Fs)
	sig_limited = np.array(bf.setNRZLevels(signal))

	print("Length initial sig", len(signal))
	
	output = bf.product_modulation(bf.setNRZLevels(signal),bf.setNRZLevels(ss_code), spreading_factor, chip_rate)
	print(output) 
	bf.file_information("transmited.txt", "w", output, signal, ss_code, spreading_factor)
	print("Length output sig", len(output))


	bf.show_signal(sig_limited, "Original Signal",ax1)
	bf.show_signal(output, "Transmited Signal",ax2)
	
	plt.show() 