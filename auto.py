import os
import sys
import csv
import operator
import json
import requests

def getCusip(jsonObj, ticker, cusip, extra):
	for elm in jsonObj:
		return(getData(jsonObj['model'], ticker, cusip, extra))

def getData(content, ticker, cusip, extra):
	data = {}

	try:
		if len(content['FundInformationData']['fundInformationData']['publicationNm']) > 0:
			data['pick'] = "Pick"
	except:
		data['pick'] = ""
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
	return('{},{},{},{},{},{},{},{},{},{},{},{}'.format(ticker, data['pick'], data['category'], data['star'], data['net'], data['ytd'], data['1yr'], data['3yr'], data['5yr'], data['10yr'], cusip, extra))

def createFiles(cont):
	words = cont.split(',')
	ticker = words[0]
	cusip = words[1]
	try:
		extra = words[2]
	except:
		extra = ""
	htmlFile = 'https://fundresearch.fidelity.com/api/mutual-funds/header/' + cusip
	response = requests.get(htmlFile)
	try:
		return(getCusip(response.json(), ticker, cusip, extra))
	except:
		return(('{} - !!!! NO DATA FOUND'.format(ticker)))

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


if __name__ == "__main__":
	if os.path.isfile("output.csv"):
		os.remove("output.csv")
	res = []

	lines = listMaker('input.csv')
	cnt = 0
	for elem in lines:
		progress(cnt, (len(lines)-1))
		cnt+=1
		res.append(createFiles(elem))

	# print(res)

	# sortList = sorted(res, key=lambda x: x.split(',')[2])
	sortList = res
	sortList.insert(0,"Ticker,Pick/Not,Category,Stars,NET,YTD,1yr,3yr,5yr,10yr,Cusip,Code")
	# sortedList = sortIt(res)
	# sortedList.insert(0,"Ticker,Pick/Not,Category,Stars,NET,YTD,1yr,3yr,5yr,10yr,Cusip,Code")


	with open('output.csv', 'w') as file_handle:
		file_handle.writelines("%s\n" % place for place in sortList)
		# file_handle.writelines("%s\n" % place for place in res)