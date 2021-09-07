
## GENERAL INFORMATION

### Title of Dataset: 
GLOBAL HEALTH MONITORING

### About
The Global Health Monitoring project aims to predict health indicators with satellite images using Deep Learning methods.

### Authors: 
Pascal Geldsetzer, Ali Lenjani, Turan Orenbas, Dorothee Mersch, Gautam M.


### Date of data collection (single date, range, approximate date): 
Multiple sources of data are collected at different times, which are elaborated for each feature in the dataset


### Geographic location of data collection: 
Multiple locations in different regions, including Africa, South America, South Asia, and Europe  
	


## SHARING/ACCESS INFORMATION

### Links to publications that cite or use the data: 

### Links to the accessible locations of the data: 

1. https://storage.cloud.google.com/global-health-monitoring/gee_hf.csv

2. https://storage.cloud.google.com/global-health-monitoring/dhs.csv

3. https://storage.cloud.google.com/global-health-monitoring/se.csv

### Links to the source that data is derived from: 
1. https://dhsprogram.com/
2. https://developers.google.com/earth-engine/datasets
3. https://www.nature.com/articles/s41591-020-1059-1 
4. https://data.un.org
5. https://databank.worldbank.org/home.aspx
6. https://ec.europa.eu/eurostat
7. https://www.kaggle.com/datasets



## DATA OVERVIEW & METHODOLOGICAL INFORMATION

This dataset is consists of multiple categories of features, including: 

A. The "ground truth" data comes from the Demographic and Health Surveys (DHS). These are nationally representative household surveys that provide the GPS for each sampled primary sampling unit (PSU; these can be thought of as villages in rural areas and neighborhoods in urban areas). For privacy reasons, the DHS jitters the GPS of each PSU by 0-2km in urban areas and 0-5km in rural areas. The DHS features include the date of the surveyed PSU and PSU-level summary measures of health indicators. For more details, please see this link: https://www.dhsprogram.com/pubs/pdf/DHSG4/Recode6_DHS_22March2013_DHSG4.pdf. Link to our PSU-level dataset: https://storage.cloud.google.com/global-health-monitoring/dhs.csv

B. Google Earth Engine (GEE) features extracted from GEE public data archived imagery and scientific datasets from different sources, including Landsat, Sentinel, and MODIS. These features are spatially and temporally matched with the DHS dataset if possible. Multiple statistical features are extracted from the 2km * 2km patches with the center located at PSU GPS. If the feature is not available for the exact date on which the DHS data were collected, then it is matched to the closest date for which the GEE feature is available. The columns in this dataset are named in the following fashion: "feature name _ statistical measure @ dataset address on GEE & timestamped(if the feature is not available for the exact time that the survey occurred)." For more information about each feature, please use this link "https://developers.google.com/earth-engine/datasets/*" and replace the * with the "dataset address on GEE" term of the column's name. Link to the data: https://storage.cloud.google.com/global-health-monitoring/gee_hf.csv
		
C. Healthcare Facility (HF) features which are extracted from a dataset published along with a paper entitled "Global maps of travel time to healthcare facilities." These features describe the motorized and walking distance to the closest healthcare facilities. These features include the average of 'walking_only_friction_surface', 'walking_only_travel_time', 'motorized_only_friction_surface', 'motorized_only_travel_time' for different radiuses around the GPS location provided for each PSU. Link to the data: https://storage.cloud.google.com/global-health-monitoring/gee_hf.csv

D. Country-level Socio-Economic (SE) features are collected from multiple sources, including UNdata, World Bank Open Data, Kaggle, and Eurostat Nations. The type of features in this dataset are highly diverse, including: 'Mean years of schooling, 'Gross national income (GNI) per capita', 'GNI per capita rank minus HDI rank', 'Change in HDI rank 2010-2015', 'Average annual HDI growth 2000-2010','Average annual HDI growth 2010-2015', 'Gender Development Index value','Gender Development Index Group', 'Human Development Index (HDI) Female', 'Human Development Index (HDI) Male', 'Life expectancy at birth Female', 'Life expectancy at birth Male', 'Mean years of schooling Female', 'Mean years of schooling Male','Estimated gross national income per capita Female', 'Estimated gross national income per capita Male', 'Share of seats in parliament (% held by women)', 'Labour force participation rate (% ages 15 and older) Female '. 
Link to the data: https://storage.cloud.google.com/global-health-monitoring/se.csv

### Instruction for merging the data and preparing it for the modeling: 

The DHS data have the "ground truth" PSU-level health indicator values that we are trying to predict. So typically, we only need to select the column of the interest, e.g., BMI, which is represented as "V445", and merge it with the GEE, HF, and SE features. The GEE and HF data are already merged together and shared here: https://storage.cloud.google.com/global-health-monitoring/gee_hf.csv. To merge the SE data, we need to match the "DHSCC" column of the GEE_HF file with the "Country Code" column of the SE data.












# Satellite Imagery Dataset

## Description of the Dataset
The BMI Satellite Imagery Dataset consists of ~55,000 satellite images and a csv file.
### CSV File
The csv file contains a row for every satellite image:
- ~55,500 rows within csv file
- A single row consists of country code, image number, cluster code, longitude and latitude of the cluster, year and BMI value:
### Satellite Images
The satellite images are stored as .tfrecord files. A single image is stored in a single tfrecord. The tfrecord contains 8 channels (bands) representing blue, green, red, NIR, SWIR ... and additionally the features of interest (country code, image number, cluster code, longitude and latitude of the cluster, year and BMI value) for safety purposes. The height and width of the images are 225px  representing 6.75 kilometers (1px = 30m). These images were taken by the Landsat satellites (NASA):
- Satellite: Landsat (NASA)
- Size of Image: 225 x 225px
- Size of ROI: 6.75 x 6.75km (1px = 30m)
- Multispectral image: blue, green, red, NIR, SWIR1, SWIR2, TEMP1
- Additional channels: country code, image number, cluster code, longitude and latitude of the cluster, year and BMI value
- Data type: tfrecord


## Accessing the Dataset
You can find the BMI Satellite Imagery Dataset on Sherlock:
- Path: https://storage.cloud.google.com/global-health-monitoring/bmi_landsat_dataset
- Dataset: Each survey per country and year has its own folder
- Folders: Each survey per country and year has a varying number of images

### Technical infos
If you have problems reading the tfrecords you can use the following code provided by us to access the tfrecords:
```python
import os
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

train_feature_description = {
  "BLUE": tf.io.FixedLenSequenceFeature([], tf.float32, allow_missing=True),
  "GREEN": tf.io.FixedLenSequenceFeature([], tf.float32, allow_missing=True),
  "RED": tf.io.FixedLenSequenceFeature([], tf.float32, allow_missing=True),
  "NIR": tf.io.FixedLenSequenceFeature([], tf.float32, allow_missing=True),
  "SWIR1": tf.io.FixedLenSequenceFeature([], tf.float32, allow_missing=True),
  "SWIR2": tf.io.FixedLenSequenceFeature([], tf.float32, allow_missing=True),
  "TEMP1": tf.io.FixedLenSequenceFeature([], tf.float32, allow_missing=True),
  "V001": tf.io.FixedLenSequenceFeature([], tf.float32, allow_missing=True),
  "V000": tf.io.FixedLenSequenceFeature([], tf.string, allow_missing=True),
  "LATNUM": tf.io.FixedLenSequenceFeature([], tf.float32, allow_missing=True),
  "LONGNUM": tf.io.FixedLenSequenceFeature([], tf.float32, allow_missing=True),
  "V445": tf.io.FixedLenSequenceFeature([], tf.float32, allow_missing=True),
  "V006": tf.io.FixedLenSequenceFeature([], tf.float32, allow_missing=True),
  "V007": tf.io.FixedLenSequenceFeature([], tf.float32, allow_missing=True),
}

def _parse_image_function(example_proto):
    return tf.io.parse_single_example(example_proto, train_feature_description)
 
train_ids = []
train_class = []
train_images = []

train_files = ["path/to/your/tfrecord"]

for i in train_files:
    train_image_dataset = tf.data.TFRecordDataset(i)

train_image_dataset = train_image_dataset.map(_parse_image_function)

# extract tfrecord features
red = [image_features['RED'].numpy() for image_features in train_image_dataset] 
green = [image_features['GREEN'].numpy() for image_features in train_image_dataset]
blue = [image_features['BLUE'].numpy() for image_features in train_image_dataset]
nir = [image_features['NIR'].numpy() for image_features in train_image_dataset]
swir1 = [image_features['SWIR1'].numpy() for image_features in train_image_dataset]
swir2 = [image_features['SWIR2'].numpy() for image_features in train_image_dataset]
temp1 = [image_features['TEMP1'].numpy() for image_features in train_image_dataset]
V001 = [image_features['V001'].numpy() for image_features in train_image_dataset]
V000 = [image_features['V000'].numpy() for image_features in train_image_dataset]
latnum = [image_features['LATNUM'].numpy() for image_features in train_image_dataset]
longnum = [image_features['LONGNUM'].numpy() for image_features in train_image_dataset]
V445 = [image_features['V445'].numpy() for image_features in train_image_dataset]
V006 = [image_features['V006'].numpy() for image_features in train_image_dataset]
V007 = [image_features['V007'].numpy() for image_features in train_image_dataset]


for i in range(len(red)):
    red = np.reshape(red[i], (225,225))
    green = np.reshape(green[i], (225,225))
    blue = np.reshape(blue[i], (225,225))
    nir = np.reshape(nir[i], (225,225))
    swir1 = np.reshape(swir1[i], (225,225))
    swir2 = np.reshape(swir2[i], (225,225))
    temp1 = np.reshape(temp1[i], (225,225))
    
    print("V001", V001[i], "V000", V000[i], "LATNUM", latnum[i], "LONGNUM", longnum[i], "V445", V445[i], "V006", V006[i], "V007", V007[i])

    rgb = np.dstack((red, green, blue))
    
print(latnum, longnum)
plt.imshow(rgb)
```python
