import urllib.request, urllib.parse, json, os, csv, datetime, re

def create_csv_file(path_graph, path_high_lows, csv_path):
	f = open(path_graph, 'r')
	data = f.read()
	#make a list with values from the .json file
	graph_data = data.split(']]')

	#order data
	for i in range(4):
		if 'price_usd' in graph_data[i][:15]:
			usd_data = graph_data[i].replace(':', '').replace('"', '').replace(']', '').replace('[', '').replace('price_usd', '')

		if 'cap' in graph_data[i][:15]:
			market_cap_data = graph_data[i].replace(':', '').replace('"', '').replace(']', '').replace('[', '').replace('market_cap_by_available_supply', '')

		if 'btc' in graph_data[i][:15]:
			price_btc_data = graph_data[i].replace(':', '').replace('"', '').replace(']', '').replace('[', '').replace('price_btc', '')

		if 'volume' in graph_data[i][:15]:
			volume_usd_data = graph_data[i].replace(':', '').replace('"', '').replace(']', '').replace('[', '').replace('volume_usd', '')

	market_cap_data = market_cap_data[1:]
	usd_data = usd_data[1:]
	price_btc_data = price_btc_data[1:]
	volume_usd_data = volume_usd_data[1:]

	#make a list with all the days that there are values from
	days = usd_data.replace(' ', '')
	days = days.split(',')
	days = int(len(days)/2 + 1)
	days = list(range(1,days))

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


	#make a list with market_cap_data
	values = market_cap_data.replace(' ', '')
	values = values.split(',')

	marketvalues = []

	i = 0
	for x in values:
		if i == 0:
			i += 1
			continue

		if i == 1:
			marketvalues.append(x)
			i = 0
			continue

	#make a list with price_btc_data
	values = price_btc_data.replace(' ', '')
	values = values.split(',')

	btcvalues = []

	i = 0
	for x in values:
		if i == 0:
			i += 1
			continue

		if i == 1:
			btcvalues.append(x)
			i = 0
			continue

	#make a list with volume_usd_data
	values = volume_usd_data.replace(' ', '')
	values = values.split(',')

	marketvolume = []

	i = 0
	for x in values:
		if i == 0:
			i += 1
			continue

		if i == 1:
			marketvolume.append(x)
			i = 0
			continue


	#Add high and lows
	f = open(path_high_lows, 'r')
	tds = f.read()
	tds = tds.split()

	#filter tds
	heighs = []
	lows = []

	i = 0
	for td in tds:
		if i==5:
			i = 0
		else:
			if i == 1:
				td = td.replace(",",'').replace("'",'')
				td = round(float(td), 2)
				heighs.append(td)

			if i == 2:
				td = td.replace(",",'').replace("'",'')
				td = round(float(td), 2)
				lows.append(td)
			i += 1

	heighs = list(reversed(heighs))
	lows = list(reversed(lows))

	#create csv itself
	csv_name = csv_path + '.csv'

	with open(csv_name, 'w') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, lineterminator = '\n')
		wr.writerow(['Day', 'Usd', 'Market_Cap', 'Btc', 'Volume', 'Heighs', 'Lows'])
		for day in days:
			wr.writerow([days[day-1], usdvalues[day-1], marketvalues[day-1], btcvalues[day-1], marketvolume[day-1], heighs[day-1], lows[day-1]])

	f.close()


def download_and_update_file(graph_link, high_lows_link, csv_path, folder, graph_file_name, high_lows_name):
	#download graph file
	with urllib.request.urlopen(graph_link) as url:
		data = json.loads(url.read().decode())

	#save graph file
	with open(folder+graph_file_name, 'w') as outfile:
		json.dump(data, outfile)

	#download page
	page = urllib.request.urlopen(high_lows_link)
	page = page.read()

	#find tds
	tds = re.findall(r'<td>(.*?)</td>', str(page))
	tds = str(tds)

	#save high_lows file
	with open(folder+high_lows_name, 'w') as outfile:
		outfile.write(tds)

	#create csv file
	create_csv_file(folder+graph_file_name, folder+high_lows_name, csv_path)

#run above code
today = str(datetime.date.today())
today = today.replace('-', '')
high_lows_link = 'https://coinmarketcap.com/currencies/ethereum/historical-data/?start=20130428&end=' + today

graph_data_link = 'https://graphs2.coinmarketcap.com/currencies/ethereum/'

#safe_folder = 'F:/python projects/ethereum predictor/V1/data/value per day/'
safe_folder = os.path.dirname(__file__) +  '/data/'

graph_data_save_name = 'ethereum.json'

high_lows_save_name = 'high_lows.txt'

csv_path = safe_folder + 'ethereum'

download_and_update_file(graph_data_link, high_lows_link, csv_path, safe_folder, graph_data_save_name, high_lows_save_name)
