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

srrs2 = pd.read_csv(srrs2_path)
srrs2.columns = srrs2.columns.map(str.strip)
srrs2.rename(columns={'cntyfips': 'ctfips'}, inplace=True)

cty = pd.read_csv(cty_path)

data = srrs2.merge(cty[['stfips', 'ctfips', 'Uppm']],
                   on=['stfips', 'ctfips'])
data.county = data.county.str.strip().str.replace(' ', '_').str.replace('.', '')
data['state_county'] = data.state + '-' + data.county
data['is_basement'] = (data.floor == 0)
data.drop_duplicates(subset=['idnum'], inplace=True)

data.county = data.county.apply(str.strip)
data.dropna(subset=['county'], inplace=True)
# counties = data.state_county.unique()
# county_lookup = dict(zip(counties, range(len(counties))))
# data['county_idx'] = data.state_county.replace(county_lookup)
data.rename(columns={'Uppm': 'county_uranium', 'activity': 'radon'},
            inplace=True)
(data[['state', 'state_county',
       # 'county_idx',
       'county_uranium', 'is_basement', 'radon']]
     .to_csv(sys.stdout, sep='\t', index=False))
