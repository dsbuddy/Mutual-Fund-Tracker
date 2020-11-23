import os
import sys
import json
import csv
import requests
from pprint import pprint


FILE_DELIMITER = ','

def ticker_to_cusip_id(ticker):
	# Find cusip ID
	endpoint = 'https://search.fidelity.com/search/getFundFactsResults?question=' + ticker
	response = requests.get(endpoint)
	html_string = ''

	# Check for valid response
	if response.status_code == 200:
		html_string = str(response.text)
	else:
		print('Error finding cusip')
		return None

	# Parse cusip from HTML page
	idx = html_string.find('https://fundresearch.fidelity.com/mutual-funds/summary/')
	idx_cusip_start = idx + len('https://fundresearch.fidelity.com/mutual-funds/summary/')
	idx_cusip_end = html_string.find('"', idx_cusip_start)
	cusip = html_string[idx_cusip_start:idx_cusip_end]
	return cusip

def process_input_data(filename):
	cnt = 0
	total =  sum(2 for line in open(filename))
	input_rows = []

	# Read in file
	with open(filename, 'r') as f:
		for line in f:
			# Update progress bar
			display_progress_bar(cnt, total, "Finding Cusip IDs")
			cnt += 1

			# Parse input
			cusip_contents = line.split(FILE_DELIMITER)
			ticker = cusip_contents[0].strip().upper()
			comments = cusip_contents[1:]
			cusip = ticker_to_cusip_id(ticker)

			# Save ticker, cusip, comments to array
			if not (cusip is None):
				input_rows.append(ticker + FILE_DELIMITER + cusip + FILE_DELIMITER + FILE_DELIMITER.join(comments))
			else:
				input_rows.append(ticker + FILE_DELIMITER + "NO VALID CUSIP ID FOUND" + FILE_DELIMITER + FILE_DELIMITER.join(comments))
	return input_rows, cnt, total

def display_progress_bar(count, total, status=''):
    bar_len = 60
    if float(total) > 0:
	    filled_len = int(round(bar_len * count / float(total)))
	    percents = round(100.0 * count / float(total), 1)
	    bar = '=' * filled_len + '-' * (bar_len - filled_len)
	    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
	    sys.stdout.flush()

def format_response_row(content):
	# Parse input rows
	ticker_contents = content.split(',')
	ticker = ticker_contents[0]
	cusip = ticker_contents[1]

	# Send HTTP request to endpoint
	endpoint = 'https://fundresearch.fidelity.com/api/mutual-funds/header/' + cusip
	response = requests.get(endpoint)
	comments = ticker_contents[2:]

	try:
		# Parse HTTP response
		response_json = response.json()['model']
		data = {}
		params = [('net',response_json['DetailsData']['detailDataList'][0]['expRatioGross']['value']),('star',response_json['MStarRatingsData']['stardata'][0]['starOverallRating']),('category',response_json['FundInformationData']['fundInformationData']['mstarCtgyName']),('ytd',response_json['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['cumulativeReturnsYtd']),('1yr',response_json['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['averageAnnualReturns1yr']),('3yr',response_json['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['averageAnnualReturns3yr']),('5yr',response_json['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['averageAnnualReturns5yr']),('10yr',response_json['PerformanceAvgAnnualReturnsData']['performanceAvgAnnualReturnsDataList'][0]['fundPerformanceRowDataList'][0]['averageAnnualReturns10yr'])]
		for param in params:
			try:
				data[param[0]] = param[1]
			except:
				data[param[0]] = "N/A"

		# Format output row as list
		col_vals = [ticker, cusip, data['category'], data['star'], data['net'], data['ytd'], data['1yr'], data['3yr'], data['5yr'], data['10yr']]
		return FILE_DELIMITER.join(col_vals) + FILE_DELIMITER + FILE_DELIMITER.join(str(x) for x in comments)
		# return FILE_DELIMITER.join("'"+x+"'" for x in col_vals) + FILE_DELIMITER + FILE_DELIMITER.join("'"+str(x)+"'" for x in comments)
	except:
		return(('{} - !!!! NO DATA FOUND\n'.format(ticker)))


def main():
	output_rows = []
	cnt = 0

	# Remove old output
	if os.path.isfile("output.csv"):
		os.remove("output.csv")

	# Parse input and compute performance details on input fields
	parsed_input, cnt, total = process_input_data('input.csv')
	for row in parsed_input:
		display_progress_bar(cnt, total, "Extracting Values")
		cnt += 1
		output_rows.append(format_response_row(row))

	# Sort by tickers and insert header row
	sorted_rows = sorted(output_rows, key=lambda x: x.split(FILE_DELIMITER)[0])
	col_names = ['Ticker','Cusip','Category','Stars','NET','YTD','1yr','3yr','5yr','10yr']
	sorted_rows.insert(0, FILE_DELIMITER.join(col_names))

	# Write all rows to csv
	with open('output.csv', 'w') as f:
		f.write("%s\n" % sorted_rows[0])
		f.writelines("%s" % row for row in sorted_rows[1:])

if __name__ == "__main__":
	main()