def create_ether_file(path):
	f = open(path, 'r')
	data = f.read()
	#print(data)

	#make a list with values from the .json file
	newdata = data.split(']]')

	market_cap_data = newdata[0].replace(':', '').replace('"', '').replace(']', '').replace('[', '').replace('market_cap_by_available_supply', '')
	price_btc_data = newdata[1].replace(':', '').replace('"', '').replace(']', '').replace('[', '').replace('price_btc', '')
	usd_data = newdata[2].replace(':', '').replace('"', '').replace(']', '').replace('[', '').replace('price_usd', '')
	volume_usd_data = newdata[3].replace(':', '').replace('"', '').replace(']', '').replace('[', '').replace('volume_usd', '')

	market_cap_data = market_cap_data[1:]
	usd_data = usd_data[1:]
	price_btc_data = price_btc_data[1:]
	volume_usd_data = volume_usd_data[1:]
	#print(newdata)

	#make a list with all the days that there are values from
	days = usd_data.replace(' ', '')
	days = days.split(',')
	days = int(len(days)/2 + 1)
	days = list(range(1,days))
	#print(len(days))

	#make a list with all the usd values
	values = usd_data.replace(' ', '')
	values = values.split(',')

	usdvalues = []

	i = 0
	for x in values:
		if i == 0:
			i += 1
			continue

		if i == 1:
			usdvalues.append(x)
			i = 0
			continue

	#print(usdvalues)
	#print(len(usdvalues))


	#create csv file with days and values for those days
	#path - .json + .csv
	csv_name = path.replace('.json', '.csv')
	print(csv_name)

	print(days[1])

	with open(csv_name, 'w') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, lineterminator = '\n')
		wr.writerow(['Day', 'Price'])
		for day in days:
			wr.writerow([days[day-1], usdvalues[day-1]])

	f.close()
