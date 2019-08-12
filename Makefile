data/clean_data.tsv: scripts/clean_raw_data.py raw/srrs2.dat raw/cty.dat
	python3 $^ > $@

