data/clean_data.tsv: scripts/clean_raw_data.py raw/srrs2.dat raw/cty.dat
	python3 $^ > $@

.init:
	git config --local filter.dropoutput_ipynb.clean scripts/ipynb_output_filter.py
	git config --local filter.dropoutput_ipynb.smudge cat
	git config --local diff.daff-csv.command "daff.py diff --git"
	git config --local merge.daff-csv.name "daff.py tabular merge"
	git config --local merge.daff-csv.driver "daff.py merge --output %A %O %A %B"
