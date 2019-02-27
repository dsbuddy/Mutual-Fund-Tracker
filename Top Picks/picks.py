import os
import sys
import json
import requests



def getPickInput(jsonObj):
	length = len(jsonObj['MFDS']['AllFunds'])
	csvList = []

	for i in range(length):
		csvList.append(getData(jsonObj['MFDS']['AllFunds'][i]))

	return csvList



def getData(content):
	data = {}
	try:
		data['ticker'] = content['FundInfo']['Ticker']
	except:
		data['ticker'] = "N/A"
	try:
		data['MFname'] = content['FundInfo']['LegalNm']
	except:
		data['MFname'] = "N/A"
	try:
		data['gross'] = content['ExpenseAndFees']['GrossXpnsRatioProspectus']
	except:
		data['gross'] = "N/A"
	try:
		data['star'] = content['FundMstarCategoryDetails']['MStarRating']['Overall']
	except:
		data['star'] = "N/A"
	try:
		data['category'] = content['FundInfo']['MstarCategoryNm']
	except:
		data['category'] = "N/A"
	try:
		data['ytd'] = content['FundPrfm']['YTD']
	except:
		data['ytd'] = "N/A"
	try:
		data['net'] = content['ExpenseAndFees']['NetXpnsRatioAnnReport']
	except:
		data['net'] = "N/A"
	try:
		data['1yr'] = content['FundPrfm']['MonthlyPrfmDetails']['AvgAnnRtrns']['Yr1']
	except:
		data['1yr'] = "N/A"
	try:
		data['3yr'] = content['FundPrfm']['MonthlyPrfmDetails']['AvgAnnRtrns']['Yr3']
	except:
		data['3yr'] = "N/A"
	try:
		data['5yr'] = content['FundPrfm']['MonthlyPrfmDetails']['AvgAnnRtrns']['Yr5']
	except:
		data['5yr'] = "N/A"
	try:
		data['10yr'] = content['FundPrfm']['MonthlyPrfmDetails']['AvgAnnRtrns']['Yr10']
	except:
		data['10yr'] = "N/A"
	return('{},{},{},{},{},{},{},{},{},{},{}'.format(data['ticker'], data['MFname'], data['category'], data['star'], data['net'], data['gross'], data['ytd'], data['1yr'], data['3yr'], data['5yr'], data['10yr']))



if __name__ == "__main__":
	response = requests.get('https://www.fidelity.com/evaluator/search?otNI=OPEN&ntf=Y&fdPks=Y&ret=5&tab=ov&sortBy=FUND_PRFM_MTH_NLD_AATR_3YR_PCT&sortDr=desc&levind=N&invind=N&fidFndRsltsMin=1&fidFndRsltsMax=3&allFndRsltsMin=1&allFndRsltsMax=400')
	data = response.json()
	res = getPickInput(data)

	if os.path.isfile("topPicks.csv"):
		os.remove("topPicks.csv")


	sortList = sorted(res, key=lambda x: x.split(',')[0])
	sortList.insert(0, "Ticker,Name,Category,Stars,NET,Gross,YTD,1yr,3yr,5yr,10yr")


	with open('topPicks.csv', 'w') as file_handle:
		file_handle.writelines("%s\n" % place for place in sortList)