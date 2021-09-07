# GHM
GENERAL INFORMATION

1. Title of Dataset: GLOBAL HEALTH MONITORING

2. Author Information
		Name: Ali Lenjani
		Institution: Stanford University
		Address: 1701 Page Mill Dr, Palo Alto
		Email: alenjani@stanford.edu

   		Name: Pascal Geldsetzer
		Institution: Stanford University
		Email: pgeldsetzer@stanford.edu


3. Date of data collection (single date, range, approximate date): Multiple sources of data are collected at different times, which are elaborated for each feature in the dataset


4. Geographic location of data collection: Multiple locations in different regions, including Africa, South America, South Asia, and Europe  
	


SHARING/ACCESS INFORMATION

1. Links to publications that cite or use the data: 

2. Links to the accessible locations of the data: 
		1. https://storage.cloud.google.com/global-health-monitoring/gee_hf.csv
		2. https://storage.cloud.google.com/global-health-monitoring/dhs.csv
		3. https://storage.cloud.google.com/global-health-monitoring/se.csv

3. Links to the source that data is derived from: 
		1. https://dhsprogram.com/
		2. https://developers.google.com/earth-engine/datasets
		3. https://www.nature.com/articles/s41591-020-1059-1 
		4. https://data.un.org
		5. https://databank.worldbank.org/home.aspx
		6. https://ec.europa.eu/eurostat
		7. https://www.kaggle.com/datasets



DATA OVERVIEW & METHODOLOGICAL INFORMATION

This dataset is consists of multiple categories of features, including: 

	A. The "ground truth" data comes from the Demographic and Health Surveys (DHS). These are nationally representative household surveys that provide the GPS for each sampled primary sampling unit (PSU; these can be thought of as villages in rural areas and neighborhoods in urban areas). For privacy reasons, the DHS jitters the GPS of each PSU by 0-2km in urban areas and 0-5km in rural areas. The DHS features include the date of the surveyed PSU and PSU-level summary measures of health indicators. For more details, please see this link: https://www.dhsprogram.com/pubs/pdf/DHSG4/Recode6_DHS_22March2013_DHSG4.pdf. Link to our PSU-level dataset: https://storage.cloud.google.com/global-health-monitoring/dhs.csv

	B. Google Earth Engine (GEE) features extracted from GEE public data archived imagery and scientific datasets from different sources, including Landsat, Sentinel, and MODIS. These features are spatially and temporally matched with the DHS dataset if possible. Multiple statistical features are extracted from the 2km * 2km patches with the center located at PSU GPS. If the feature is not available for the exact date on which the DHS data were collected, then it is matched to the closest date for which the GEE feature is available. The columns in this dataset are named in the following fashion: "feature name _ statistical measure @ dataset address on GEE & timestamped(if the feature is not available for the exact time that the survey occurred)." For more information about each feature, please use this link "https://developers.google.com/earth-engine/datasets/*" and replace the * with the "dataset address on GEE" term of the column's name. Link to the data: https://storage.cloud.google.com/global-health-monitoring/gee_hf.csv
		
	C. Healthcare Facility (HF) features which are extracted from a dataset published along with a paper entitled "Global maps of travel time to healthcare facilities." These features describe the motorized and walking distance to the closest healthcare facilities. These features include the average of 'walking_only_friction_surface', 'walking_only_travel_time', 'motorized_only_friction_surface', 'motorized_only_travel_time' for different radiuses around the GPS location provided for each PSU. Link to the data: https://storage.cloud.google.com/global-health-monitoring/gee_hf.csv

	D. Country-level Socio-Economic (SE) features are collected from multiple sources, including UNdata, World Bank Open Data, Kaggle, and Eurostat Nations. The type of features in this dataset are highly diverse, including: 'Mean years of schooling, 'Gross national income (GNI) per capita', 'GNI per capita rank minus HDI rank', 'Change in HDI rank 2010-2015', 'Average annual HDI growth 2000-2010','Average annual HDI growth 2010-2015', 'Gender Development Index value','Gender Development Index Group', 'Human Development Index (HDI) Female', 'Human Development Index (HDI) Male', 'Life expectancy at birth Female', 'Life expectancy at birth Male', 'Mean years of schooling Female', 'Mean years of schooling Male','Estimated gross national income per capita Female', 'Estimated gross national income per capita Male', 'Share of seats in parliament (% held by women)', 'Labour force participation rate (% ages 15 and older) Female '. 
Link to the data: https://storage.cloud.google.com/global-health-monitoring/se.csv

Instruction for merging the data and preparing it for the modeling: 

	The DHS data have the "ground truth" PSU-level health indicator values that we are trying to predict. So typically, we only need to select the column of the interest, e.g., BMI, which is represented as "V445", and merge it with the GEE, HF, and SE features. The GEE and HF data are already merged together and shared here: https://storage.cloud.google.com/global-health-monitoring/gee_hf.csv. To merge the SE data, we need to match the "DHSCC" column of the GEE_HF file with the "Country Code" column of the SE data.
