#!/bin/bash

rm -rf mutFund.csv

echo "Ticker,Category,Star,Net,YTD,1yr,3yr,5yr,10yr" >> mutFund.csv
for name in $(cat input.txt) ; do
	python3 fund.py $name >> mutFund.csv
done
