import base_functions as bf
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':

	#file_to_read = input('What file should i read signal from?')
	file_to_read = 'channel.txt'
	channel_info = []
	recv_cdma = bf.get_information(file_to_read, 0)
	n_sig = 0
	info=1

	#-> [[sig 0,[mensagem][code][fator]],[sig 1,[mensagem][code][fator]],[sig2,[mensagem][code][fator]],[sig 3].....]
	while True:
		try:
			print(info)
			channel_info.append([n_sig])
			channel_info[n_sig].append(bf.get_information(file_to_read,info))
			channel_info[n_sig].append(bf.get_information(file_to_read,info+1))
			channel_info[n_sig].append(bf.get_information(file_to_read,info+2))			
			info+=3
			n_sig+=1
			bf.get_information(file_to_read,info)
					
		except Exception as e:
			print(e)
			break

	

	for signal_info in channel_info:
		print(signal_info[1])
		print(signal_info[2])
		print(signal_info[3])
		fig,(ax3,ax4,ax5) = plt.subplots(3)
		initial_message = signal_info[1]
		spreading_code = signal_info[2]
		spreading_factor=signal_info[3]

		Fs = int(len(recv_cdma)/len(initial_message))
		print(Fs)
		chip_rate = int(int(Fs)/int(spreading_factor[0]))
		ss = bf.spreading_sequence(len(recv_cdma), spreading_code, chip_rate)
		ss_nrz = bf.setNRZLevels(ss)
		result_signal = bf.product_modulation_r(recv_cdma, ss_nrz)
		result_message = bf.integrate_signal(result_signal, Fs)
		ber = bf.signal_comp(initial_message, result_message)



		print("INITIAL message: ", len(initial_message))
		print("result_message: ", len(result_message))
		print("Bit error rate= "+ str(ber*100)+"%")
		bf.show_signal(recv_cdma, "Received Signal",ax3)
		bf.show_signal(initial_message, "Original Message", ax4)
		bf.show_signal(result_message, "Final received message", ax5)


		plt.show() 

	# print(recv_cdma)
	# print('Spreading Sequence:')
	# print(ss)
	# print(ss_nrz)
	# print('RESULT: %s' % result_signal)
	


	