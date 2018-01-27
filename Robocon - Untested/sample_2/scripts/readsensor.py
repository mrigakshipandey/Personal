def read_sensor(i):

	# get the global values raingg gmin and wmax
	
	filer = open('raingg', "rb")
	raingg=pickle.load(raingg, filer)
	filer.close()

	filer = open('wmax', "rb")
	wmax=pickle.load(wmax, filer)
	filer.close()

	filer = open('gmin', "rb")
	gmin=pickle.load(gmin, filer)
	filer.close()

	index = 0
	for j in range(8):

		'''
		if i == 2:
			index = 7 - j
		else:
		'''
		# uncomment & indent in case of exceptions
		index = j		
		
		# normalize (if reading less than min assign 0, more than max assigm 100)

		values[i][index] = mcp[i].read_adc(index)
		if values[i][index]>=wmax[i]:
			values[i][index]=100

		elif values[i][index]>=gmin[i]:
			values[i][index]=0

		else:
			values[i][index]=((values[i][index]-gmin[i])/raingg[i])*100
		
