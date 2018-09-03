import sys
import json
import requests

def readJSONFile(filename):
	with open(filename, 'r') as f:
		jsonObj = json.load(f)
	return getCusip(jsonObj)

def getCusip(jsonObj, ticker):
	for elm in jsonObj:
		return jsonObj[ticker]['Cusip']

def readTickers(filename):
	with open(filename) as f:
		content = f.readline()
	content = [x.strip() for x in content]

def tickerToCusip(content):
	ll = []
	for ticker in content:
		ll.append(ticker + ":" + getCusip(readJSONFile((ticker+".json)"))))

def createFiles(filename):
	content = []
	with open(filename, 'r') as ins:
		for line in ins:
			line=line.strip()
			jsonFile = line + ".json"
			params = (
			    ('fIds', line),
			)
			response = requests.get('https://www.fidelity.com/evaluator/compare', params=params)

			res = []

			if line in response.json().keys():
				# print(line + "," + getCusip(response.json(), line))
				res.append(line + "," + getCusip(response.json(), line))
			else:
				# print(line)
				res.append(line)

			with open('tickersCusips.txt', 'w') as file_handler:
			    for item in res:
			    	print(item)
			    	file_handler.write("{}\n".format(item))

def getCusip2(jsonObj):
	for elm in jsonObj:
		getData(jsonObj['model'])

def getData(content):
	data = {}
	data['net'] = content['DetailsData']['detailDataList'][0]['expRatioGross']['value']
	data['star'] = content['MStarRatingsData']['stardata'][0]['starOverallRating']
	data['category'] = content['FundInformationData']['fundInformationData']['mstarCtgyName']
	data['ytd'] = content['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['cumulativeReturnsYtd']
	data['1yr'] = content['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['averageAnnualReturns1yr']
	data['3yr'] = content['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['averageAnnualReturns3yr']
	data['5yr'] = content['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['averageAnnualReturns5yr']
	data['10yr'] = content['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['averageAnnualReturns10yr']
	# print(data)
	print('{} {} {} {} {} {} {} {}'.format(data['category'], data['star'], data['net'], data['ytd'], data['1yr'], data['3yr'], data['5yr'], data['10yr']))

def createFiles2(cusip):
	htmlFile = 'https://fundresearch.fidelity.com/api/mutual-funds/header/' + cusip
	response = requests.get(htmlFile)
	getCusip2(response.json())




def getCusip3(jsonObj, ticker):
	for elm in jsonObj:
		return(getData2(jsonObj['model'], ticker))

def getData2(content, ticker):
	data = {}
	try:
		data['net'] = content['DetailsData']['detailDataList'][0]['expRatioGross']['value']
	except:
		data['net'] = "N/A"
	try:
		data['star'] = content['MStarRatingsData']['stardata'][0]['starOverallRating']
	except:
		data['star'] = "N/A"

	try:
		data['category'] = content['FundInformationData']['fundInformationData']['mstarCtgyName']
	except:
		data['category'] = "N/A"

	try:
		data['ytd'] = content['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['cumulativeReturnsYtd']
	except:
		data['ytd'] = "N/A"

	try:
		data['net'] = content['DetailsData']['detailDataList'][0]['expRatioGross']['value']
	except:
		data['net'] = "N/A"

	try:
		data['1yr'] = content['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['averageAnnualReturns1yr']
	except:
		data['1yr'] = "N/A"
	
	try:
		data['3yr'] = content['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['averageAnnualReturns3yr']
	except:
		data['3yr'] = "N/A"

	try:
		data['5yr'] = content['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['averageAnnualReturns5yr']
	except:
		data['5yr'] = "N/A"
	
	try:
		data['10yr'] = content['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['averageAnnualReturns10yr']
	except:
		data['10yr'] = "N/A"
	# print(data)
	# print('{} {} {} {} {} {} {} {} {}'.format(ticker, data['category'], data['star'], data['net'], data['ytd'], data['1yr'], data['3yr'], data['5yr'], data['10yr']))
	

	# print('{},{},{},{},{},{},{},{},{}'.format(ticker, data['category'], data['star'], data['net'], data['ytd'], data['1yr'], data['3yr'], data['5yr'], data['10yr']))
	return('{},{},{},{},{},{},{},{},{}'.format(ticker, data['category'], data['star'], data['net'], data['ytd'], data['1yr'], data['3yr'], data['5yr'], data['10yr']))
	

def createFiles3(cont):
	words = cont.split(',')
	ticker = words[0]
	cusip = words[1]
	htmlFile = 'https://fundresearch.fidelity.com/api/mutual-funds/header/' + cusip
	response = requests.get(htmlFile)
	try:
		return(getCusip3(response.json(), ticker))
	except:
		return(('{} - !!!! NO DATA FOUND'.format(ticker)))

def listMaker(filename):
	with open(filename) as f:
		lines = f.read().splitlines()
	return lines





if __name__ == "__main__":
	# createFiles(sys.argv[1])
	# createFiles2(sys.argv[1])

	res = []
	res.append("Ticker,Category,Stars,NET,YTD,1yr,3yr,5yr,10yr")

	lines = listMaker('input.csv')
	for elem in lines:
		res.append(createFiles3(elem))

	# print(res)
	with open('output.csv', 'w') as file_handle:
		file_handle.writelines("%s\n" % place for place in res)
