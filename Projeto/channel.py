import base_functions as bf

if __name__ == '__main__':

	file_to_read = 'transmited.txt'

	cdma_sig = bf.get_information(file_to_read, 0)
	initial_message = bf.get_information(file_to_read,1)
	spreading_code = bf.get_information(file_to_read,2)
	spreading_factor = bf.get_information(file_to_read,3)

	at_cdma_sig = bf.add_atenuation(cdma_sig, 0.8)
	final_sig = bf.add_whitenoise(at_cdma_sig, 0.5)
	channel_sig = []
	for bit in final_sig:
		channel_sig.append("{:.2f}".format(bit))
	bf.file_information("channel.txt", "a",channel_sig, initial_message, spreading_code, spreading_factor[0])