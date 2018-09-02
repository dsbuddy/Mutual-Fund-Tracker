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
		getData2(jsonObj['model'], ticker)

def getData2(content, ticker):
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
	# print('{} {} {} {} {} {} {} {} {}'.format(ticker, data['category'], data['star'], data['net'], data['ytd'], data['1yr'], data['3yr'], data['5yr'], data['10yr']))
	print('{},{},{},{},{},{},{},{},{}'.format(ticker, data['category'], data['star'], data['net'], data['ytd'], data['1yr'], data['3yr'], data['5yr'], data['10yr']))
	

def createFiles3(cont):
	words = cont.split(',')
	ticker = words[0]
	cusip = words[1]
	htmlFile = 'https://fundresearch.fidelity.com/api/mutual-funds/header/' + cusip
	response = requests.get(htmlFile)
	try:
		getCusip3(response.json(), ticker)
	except:
		print('{} - !!!! NO DATA FOUND'.format(ticker))





if __name__ == "__main__":
	# readJSONFile(sys.argv[1])


	# createFiles(sys.argv[1])
	# createFiles2(sys.argv[1])
	createFiles3(sys.argv[1])













		# print(jsonObj['model']['DetailsData']['detailDataList'][0]['expRatioGross']['value']) #NET
		# print(jsonObj['model']['MStarRatingsData']['stardata'][0]['starOverallRating']) #star
		# print(jsonObj['model']['FundInformationData']['fundInformationData']['mstarCtgyName']) #category
		# print(jsonObj['model']['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['cumulativeReturnsYtd']) #ytd
		# print(jsonObj['model']['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['averageAnnualReturns1yr']) #1yr
		# print(jsonObj['model']['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['averageAnnualReturns3yr']) #3yr
		# print(jsonObj['model']['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['averageAnnualReturns5yr']) #5yr
		# print(jsonObj['model']['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['averageAnnualReturns10yr']) #10yr










'''
def getData(jsonObj):
	for elm in jsonObj:
		# print(jsonObj['FAGIX']['Cusip'])
		# print(jsonObj[ticker]['Cusip'])
		
		# return jsonObj['model']
		print(elm)
		# print(jsonObj['FAGIX']['Cusip'])
		# print(jsonObj[ticker]['Cusip'])
	# print(jsonObj['model']['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'])

def getData(cusip):
	htmlFile = "https://fundresearch.fidelity.com/api/mutual-funds/header/" + cusip
	response = requests.get(htmlFile)
	# print(response.json())
	getData(response.json())

	# getData(response.json())


'''








#FAGIX
'''
Stars = 5
YTD = 2.42
1 Yr = 5.31
3 Yr = 7.20
5 Yr = 7.27
10 Yr = 9.00
NET = 0.67
Ticker

'''