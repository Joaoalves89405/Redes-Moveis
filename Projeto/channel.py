import base_functions as bf
import os
from os import listdir
from os.path import isfile,join


def add_channel_effects(signal, atenuation, whitenoise):
	channel_sig = []
	at_cdma_sig = bf.add_atenuation(signal, atenuation)
	final_sig = bf.add_whitenoise(at_cdma_sig, whitenoise)
	for bit in final_sig:
		channel_sig.append("{:.2f}".format(bit))
	with open('channel.txt', 'w') as f_channel, open('temp.txt','r+') as temp:
		f_channel.seek(0,0)
		for bit in channel_sig[:-1]:
			f_channel.write("%s," % str(bit))
		f_channel.write("%s\n" % str(channel_sig[-1]))
		for line in temp:
			f_channel.write(line)
		os.remove("temp.txt")

if __name__ == '__main__':

	file_path = "./transmited/"
	files_to_read = [file_path+f for f in listdir(file_path) if isfile(join(file_path, f))]
	signal_sum=[]

	for file in files_to_read:
		cdma_sig = bf.get_information(file, 0)
		initial_message = bf.get_information(file,1)
		spreading_code = bf.get_information(file,2)
		spreading_factor = bf.get_information(file,3)
		if not signal_sum:
			signal_sum.extend(cdma_sig)
			bf.file_information("temp.txt", "a",None, initial_message, spreading_code, spreading_factor[0])
		else:
			for indx, bit in enumerate(cdma_sig):
				signal_sum[indx] = bit+signal_sum[indx]
			bf.file_information('temp.txt','a',None,initial_message, spreading_code,spreading_factor[0])
	add_channel_effects(signal_sum, 0.1, 0.3)
	