DATE=`date`

upload:
	git add plots/
	git add data/
	git add documents/
	git commit -m "Update plot at ${DATE}"
	git push origin master

update:
	python3 scripts/update_v5.py
	python3 scripts/parse_v5.py
	#python3 scripts/update_nyc_v5.py
	python3 scripts/parse_nyc_v5.py
	python3 scripts/dump.py
	# python3 scripts/plot.py
	python3 scripts/plot_v2.py
	python3 scripts/plot2.py

update-pdf:
	python3 scripts/extract_nyc_pdf.py documents/NYC-covid-19-daily-data-summary data/NYC-covid-19-daily-data-summary.csv
	python3 scripts/extract_nyc_pdf.py documents/NYC-covid-19-daily-data-summary-deaths data/NYC-covid-19-daily-data-summary-deaths.csv
