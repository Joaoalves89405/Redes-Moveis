import base_functions as bf
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
	
	fig,(ax3,ax4,ax5) = plt.subplots(3)


	#file_to_read = input('What file should i read signal from?')
	file_to_read = 'channel.txt'
	recv_cdma = bf.get_information(file_to_read, 0)
	initial_message = bf.get_information(file_to_read,1)
	spreading_code = bf.get_information(file_to_read,2)
	spreading_factor = bf.get_information(file_to_read,3)

	Fs = int(len(recv_cdma)/len(initial_message))
	chip_rate = int(int(Fs)/int(spreading_factor[0]))

	ss = bf.spreading_sequence(len(recv_cdma), spreading_code, chip_rate)
	print(recv_cdma)
	print('Spreading Sequence:')
	print(ss)
	ss_nrz = bf.setNRZLevels(ss)
	print(ss_nrz)
	result_signal = bf.product_modulation_r(recv_cdma, ss_nrz)
	print('RESULT: %s' % result_signal)
	
	result_message = bf.integrate_signal(result_signal, Fs)
	print("INITIAL message: ", len(initial_message))
	print("result_message: ", len(result_message))
	ber = bf.signal_comp(initial_message, result_message)
	print("Bit error rate= ", ber)


	bf.show_signal(recv_cdma, "Received Signal",ax3)
	bf.show_signal(result_message, "Final received message", ax4)
	bf.show_signal(result_message, "Message Received", ax5)

	plt.show() 