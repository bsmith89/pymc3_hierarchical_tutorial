#!/usr/bin/env python3
"""
Data munging code taken almost verbatim from
<https://github.com/fonnesbeck/multilevel_modeling>

USAGE:
    python3 clean_raw_data.py [srrs2.dat] [cty.dat] > [clean_data.tsv]
"""

import sys
import pandas as pd
import numpy as np

srrs2_path = sys.argv[1]
cty_path = sys.argv[2]

# First, we import the data from a local file, and extract Minnesota's data.
srrs2 = pd.read_csv(srrs2_path)
srrs2.columns = srrs2.columns.map(str.strip)
srrs_mn = srrs2[srrs2.state == 'MN'].copy()

# Next, obtain the county-level predictor, uranium, by combining two variables.
srrs_mn['fips'] = srrs_mn.stfips * 1000 + srrs_mn.cntyfips
cty = pd.read_csv(cty_path)
cty_mn = cty[cty.st == 'MN'].copy()
cty_mn['fips'] = 1000 * cty_mn.stfips + cty_mn.ctfips

# Use the `merge` method to combine home- and county-level information in a single DataFrame.
srrs_mn = srrs_mn.merge(cty_mn[['fips', 'Uppm']], on='fips')
srrs_mn = srrs_mn.drop_duplicates(subset='idnum')

# We also need a lookup table (`dict`) for each unique county, for indexing.
srrs_mn.county = srrs_mn.county.map(str.strip)
mn_counties = srrs_mn.county.unique()
county_lookup = dict(zip(mn_counties, range(len(mn_counties))))

# Finally, create local copies of variables.
srrs_mn['county_idx'] = srrs_mn.county.replace(county_lookup).values

out = srrs_mn[['floor', 'county', 'county_idx', 'Uppm', 'activity']]
out.rename(columns={'Uppm': 'county_uranium', 'activity': 'radon'}, inplace=True)
out.to_csv(sys.stdout, sep='\t', index=False)
