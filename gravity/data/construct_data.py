"""
Prepare Gravity Dataset for Econometrics Textbook

Data Sources
------------
1. 	SITC Rev. 2 Data (The Observatory of Economic Complexity - MIT)
	Website: http://atlas.media.mit.edu/en/resources/data/
	Files: 
		year_origin_destination_sitc_rev2.tsv 	MD5: 056a7a32b6b97c993810b08eda96f4a8

2.  Geographic Data from CEPII
	Website: http://www.cepii.fr/CEPII/en/bdd_modele/presentation.asp?id=6 
	Files:
		dist_cepii.xls		MD5: b52d05723746fe94459855806ab380e6
		geo_cepii.xls		MD5: 6de49a39f6e5f22e84fb512b20831aff

3. 	World Development Indicators from World Bank
	Website: http://data.worldbank.org/data-catalog/world-development-indicators
	Files:
		WDI_Data.csv 		MD5: 4bd234b12ee21e2b6b5f4a733230fa9c

Notes
-----
1. 	The data source is currently available for 1962 to 2013.
	Due to the large size of the dataset it needs to be downloaded
	from the source and uncompressed.
"""

import pandas as pd

#-Trade Data-#
trade = pd.read_csv('year_origin_destination_sitc_rev2.tsv', sep='\t')
trade = trade.rename_axis({ "year" : 'y',
							"origin" : 'i', 
							"destination" : 'j',
							"sitc_rev2" : 'p',
							"export_val" : 'ex',
							"import_val" : 'im',
							})
#-Year: 2013-#
data = trade[trade.y == 2013]
data = data.groupby(["y","i","j"]).sum()

geo = pd.read_excel('geo_cepii.xls')
dist = pd.read_excel('dist_cepii.xls')
