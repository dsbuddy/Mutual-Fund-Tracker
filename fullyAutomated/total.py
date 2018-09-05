import os
import sys
import json
import requests


def getCusip(jsonObj, ticker):
	for elm in jsonObj:
		return jsonObj[ticker]['Cusip']

def createCusipFiles(filename):
	cnt = 0
	content = []
	res = []
	total = sum(1 for line in open(filename))
	with open(filename, 'r') as ins:
		for line in ins:
			progress(cnt, ((total*2)-1), "Finding Cusip IDs")
			cnt+=1

			line=line.strip()
			jsonFile = line + ".json"
			params = (
			    ('fIds', line),
			)
			response = requests.get('https://www.fidelity.com/evaluator/compare', params=params)


			if line in response.json().keys():
				res.append(line + "," + getCusip(response.json(), line))
			else:
				res.append(line + ",NO VALID CUSIP ID FOUND")


	if os.path.isfile("tickersCusips.csv"):
		os.remove("tickersCusips.csv")

	with open('tickersCusips.csv', 'w') as file_handler:
	    for item in res:
	    	progress(cnt, ((len(res)*2)-1), "Finding Cusip IDs")
	    	cnt+=1
	    	file_handler.write("{}\n".format(item))

def listMaker(filename):
	with open(filename) as f:
		lines = f.read().splitlines()
	return lines

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() 













def getCusip2(jsonObj, ticker):
	for elm in jsonObj:
		return(getData(jsonObj['model'], ticker))

def getData(content, ticker):
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
	return('{},{},{},{},{},{},{},{},{}'.format(ticker, data['category'], data['star'], data['net'], data['ytd'], data['1yr'], data['3yr'], data['5yr'], data['10yr']))

def createFiles(cont):
	words = cont.split(',')
	ticker = words[0]
	cusip = words[1]
	htmlFile = 'https://fundresearch.fidelity.com/api/mutual-funds/header/' + cusip
	response = requests.get(htmlFile)
	try:
		return(getCusip2(response.json(), ticker))
	except:
		return(('{} - !!!! NO DATA FOUND'.format(ticker)))


if __name__ == "__main__":
	lines = createCusipFiles('tickers.txt')
	if os.path.isfile("output.csv"):
		os.remove("output.csv")
	res = []

	lines = listMaker('tickersCusips.csv')
	cnt = 0
	for elem in lines:
		progress(cnt, (len(lines)-1), "Calculating Performance Details")
		cnt+=1
		res.append(createFiles(elem))

	sortList = sorted(res, key=lambda x: x.split(',')[2])
	sortList.insert(0, "Ticker,Category,Stars,NET,YTD,1yr,3yr,5yr,10yr")


	with open('output.csv', 'w') as file_handle:
		file_handle.writelines("%s\n" % place for place in sortList)

	if os.path.isfile("tickersCusips.csv"):
		os.remove("tickersCusips.csv")

