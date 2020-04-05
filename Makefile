DATE=`date`

pull:
	git pull origin master

upload: 
	git add plots/
	git add data/
	git add documents/
	git commit -m "Update plot at ${DATE}"
	git push origin master

update-nys: pull
	python3 scripts/update_v5.py
	python3 scripts/parse_v5.py
	#python3 scripts/update_nyc_v5.py
	python3 scripts/parse_nyc_v5.py
	python3 scripts/dump.py
	# python3 scripts/plot.py
	python3 scripts/plot_v2.py
	python3 scripts/plot2.py
	python3 scripts/plot_increase_nys.py

update-pdf: pull
	python3 scripts/save_nyc_pdf_v2.py
	python3 scripts/extract_nyc_pdf.py documents/NYC-covid-19-daily-data-summary data/NYC-covid-19-daily-data-summary.csv 1
	python3 scripts/extract_nyc_pdf.py documents/NYC-covid-19-daily-data-summary-deaths data/NYC-covid-19-daily-data-summary-deaths.csv -1
	python3 scripts/extract_nyc_pdf.py documents/NYC-covid-19-daily-data-summary-hospitalizations data/NYC-covid-19-daily-data-summary-hospitalizations.csv 1
	python3 scripts/plot3.py
	python3 scripts/plot4.py
	python3 scripts/plot5.py
	python3 scripts/plot_increase_nyc.py
	python3 scripts/extract_nyc_test_by_zcta.py
	# python3 scripts/extract_map_nyc.py

update: update-pdf

update-remote: pull
	python3 scripts/save_nyc_pdf_v2.py

upload-remote: update-remote upload
upload-laptop: update-pdf upload
