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

2. 	Using dask

	#Using Chunks
	# iter_csv = pd.read_csv('year_origin_destination_sitc_rev2.tsv', sep='\t', iterator=True, chunksize=100000)
	# df = pd.concat([chunk[chunk['year'] == 2013] for chunk in iter_csv])
	# df = df[['year','origin','destination','export_val','import_val']].groupby(["year","origin","destination"]).sum()

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
"""

import pandas as pd
import dask.dataframe as dd

#------------#
#-Trade Data-#
#------------#
# trade = dd.read_csv("year_origin_destination_sitc_rev2.tsv", sep="\t", header=0)
#-Year: 2013-#
# trade = trade[trade.year == 2013]
# trade = trade[['year','origin','destination','export_val','import_val']].groupby(["year","origin","destination"]).sum()
# trade = trade.compute()

#-Chunks-#
#-Year: 2013-#
iter_csv = pd.read_csv('year_origin_destination_sitc_rev2.tsv', sep='\t', iterator=True, chunksize=100000)
trade = pd.concat([chunk[chunk['year'] == 2013] for chunk in iter_csv])
trade = trade[['year','origin','destination','export_val','import_val']].groupby(["year","origin","destination"]).sum()
#-Correct Country Codes-#
trade = trade.reset_index()
trade.origin = trade.origin.apply(lambda x: x.upper())
trade.destination = trade.destination.apply(lambda x: x.upper())

#-Export and Import Data-#
data = trade.copy()
ex = data[["year","origin","destination","export_val"]].rename(columns={'export_val':'value','origin':'eiso3c','destination':'iiso3c'})
im = data[["year","origin","destination","import_val"]].rename(columns={'import_val':'value','origin':'iiso3c','destination':'eiso3c'})

#----------------#
#-Attribute Data-#
#----------------#

#-Merge Importer Reported Data Together-#
dataset = im.copy()

#-Bilateral Relationships-#
dist = pd.read_excel('dist_cepii.xls')
bilat_attrs = ["iso_o","iso_d","contig","comlang_off","colony","dist","distcap","distw","distwces"]
dataset = dataset.merge(dist[bilat_attrs], left_on=["eiso3c","iiso3c"], right_on=["iso_o","iso_d"], how="inner")
for item in ["iso_o","iso_d"]:
	del dataset[item]

#-Country Attributes-#
geo = pd.read_excel('geo_cepii.xls')
cntry_attrs = ["iso3","landlocked"]
dataset = dataset.merge(geo[cntry_attrs], left_on="eiso3c", right_on="iso3", how="inner")
del dataset["iso3"]
dataset.rename(columns={'landlocked':'ell'}, inplace=True)
dataset = dataset.merge(geo[cntry_attrs], left_on="iiso3c", right_on="iso3", how="inner")
del dataset["iso3"]
dataset.rename(columns={'landlocked':'ill',}, inplace=True)

#-WDI-#
wdi = pd.read_csv('WDI_Data.csv')
idx = ["Country Code","Indicator Code"]
years = ["2013"]
wdi = wdi[idx+years]
wdi.columns = ["iso3c","code","value"]
wdi = wdi.set_index(["iso3c","code"]).unstack("code")
wdi.columns = wdi.columns.droplevel()
# NY.GDP.MKTP.KD = GDP (constant 2005 US$)
# NY.GDP.PCAP.KD = GDP per capita (constant 2005 US$)
codes = ['NY.GDP.MKTP.KD','NY.GDP.PCAP.KD', 'SP.POP.TOTL']
wdi_data = wdi[codes]
wdi_data.columns = ['egdp', 'egdppc','epop']
wdi_data = wdi_data.reset_index()
dataset = dataset.merge(wdi_data, left_on="eiso3c", right_on="iso3c")
del dataset['iso3c']
wdi_data = wdi[codes]
wdi_data.columns = ['igdp', 'igdppc','ipop']
wdi_data = wdi_data.reset_index()
dataset = dataset.merge(wdi_data, left_on="iiso3c", right_on="iso3c")
del dataset['iso3c']

#-Save Dataset-#
dataset.to_csv("gravity_dataset_2013.csv", index=False)

#--------- Notes ----------#

# Note: This dataset contains exporter AND importer reports so should just use exports OR imports
	# Compare Exporter and Importer Reports
	# ex, im = data["ex"].to_frame(), data["im"].to_frame().reset_index()
	# im.rename(columns={"i":"j","j":"i"}, inplace=True)
	# im.set_index(["y","i","j"], inplace=True)
	# im.sort_index(inplace=True)
	# ex.rename(columns={'ex':'v'}, inplace=True)
	# im.rename(columns={'im':'v'}, inplace=True)
	# data = ex.append(im)
