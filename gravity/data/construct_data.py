"""
Prepare Gravity Dataset for Econometrics Textbook

Data Sources
-----------
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
import dask.dataframe as dd

#-Trade Data-#
trade = dd.read_csv("year_origin_destination_sitc_rev2.tsv", sep="\t", header=0)
trade = trade.rename(columns={ "year" : 'y',
							"origin" : 'i',
							"destination" : 'j',
							"sitc_rev2" : 'p',
							"export_val" : 'ex',
							"import_val" : 'im',
							})
#-Year: 2013-#
trade = trade[trade.y == 2013]
trade = trade[['y','i','j','ex','im']].groupby(["y","i","j"]).sum()
trade = trade.compute()
#-Correct Country Codes-#
trade = trade.reset_index()
trade.i = trade.i.apply(lambda x: x.upper())
trade.j = trade.j.apply(lambda x: x.upper())

	#-Equivalent Pandas Code takes ~18GB RAM due to pandas copies
	# trade = pd.read_csv('year_origin_destination_sitc_rev2.tsv', sep='\t')
	# trade = trade.rename(columns={ "year" : 'y',
	# 							"origin" : 'i',
	# 							"destination" : 'j',
	# 							"sitc_rev2" : 'p',
	# 							"export_val" : 'ex',
	# 							"import_val" : 'im',
	# 							})
	# #-Year: 2013-#
	# data2 = trade[trade.y == 2013]
	# data2 = data[['y','i','j','ex','im']].groupby(["y","i","j"]).sum()

# Note: This dataset contains exporter AND importer reports so should just use exports OR imports
	# Compare Exporter and Importer Reports
	# ex, im = data["ex"].to_frame(), data["im"].to_frame().reset_index()
	# im.rename(columns={"i":"j","j":"i"}, inplace=True)
	# im.set_index(["y","i","j"], inplace=True)
	# im.sort_index(inplace=True)
	# ex.rename(columns={'ex':'v'}, inplace=True)
	# im.rename(columns={'im':'v'}, inplace=True)
	# data = ex.append(im)
data = trade.copy()
ex = data[["y","i","j","ex"]].rename(columns={'ex':'value','i':'eiso3c','j':'iiso3c','y':'year'})
im = data[["y","i","j","im"]].rename(columns={'im':'value','i':'iiso3c','j':'eiso3c','y':'year'})

#-Get Attribute Data-#
geo = pd.read_excel('geo_cepii.xls')
dist = pd.read_excel('dist_cepii.xls')
wdi = pd.read_csv('WDI_Data.csv')

#-Merge Importer Reported Data Together-#
dataset = im.copy()
#-Bilateral Relationships-#
# TODO
#-Country Attributes-#
cntry_attrs = ["iso3","landlocked"]
dataset = dataset.merge(geo[cntry_attrs], left_on="eiso3c", right_on="iso3", how="left")
del dataset["iso3"]
dataset.rename(columns={'landlocked':'ell'}, inplace=True)
dataset = dataset.merge(geo[cntry_attrs], left_on="iiso3c", right_on="iso3", how="left")
del dataset["iso3"]
dataset.rename(columns={'landlocked':'ill',}, inplace=True)
