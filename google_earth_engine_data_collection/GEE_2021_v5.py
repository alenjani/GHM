import ee
import warnings
import time
import datetime
import numpy as np
import urllib3
import requests
warnings.filterwarnings("ignore")
# ee.Authenticate()  # do it once before starting the script, the key is AIzaSyDn8_Ywy2dDQqW6I6M5D5xVlAIYQUeQzoA
# 4/1AfDhmrgPmgj6wz6QBQRIF2hg1WcHDVOo_zbBTUd72jUC_1VIfRcDDXQrQsg
# init the ee object
ee.Initialize()

# print(ee.data.listImages(parent, params, callback))
# print(ee.ImageCollection("LANDSAT"))

def get_rect_and_center(coords):
    if isinstance(coords[1], int):
        # If center and rect_size is given

        center_lat, center_long = coords[0]

        # not exact conversion from meters to decimal degrees but close to equator it applies very well
        # Source: https://en.wikipedia.org/wiki/Decimal_degrees
        rect_size = coords[1] / 111320
        rect = ee.Geometry.Rectangle(center_long - rect_size / 2, center_lat + rect_size / 2,
                                     center_long + rect_size / 2, center_lat - rect_size / 2)

    else:
        # If corners are given

        top_left_lat, top_left_long = coords[0]
        bot_right_lat, bot_right_long = coords[1]

        rect = ee.Geometry.Rectangle(top_left_long, top_left_lat, bot_right_long, bot_right_lat)

        center_long = (top_left_long + bot_right_long) / 2
        center_lat = (top_left_lat + bot_right_lat) / 2

    return rect, center_lat, center_long


def get_data_rapidly_new(data, geo_df_row):

    coords = [(geo_df_row['LATNUM'], geo_df_row['LONGNUM']), 2000]

    time_frame = ['{}-01'.format(int(geo_df_row['DHSYEAR']) - 1), '{}-01'.format(int(geo_df_row['DHSYEAR']))]

    # Determine the rectangle to cut out and the center point
    rect, center_lat, center_long = get_rect_and_center(coords)
    # Repeat for each pair of dataset, parameter
    ee_reducers = [ee.Reducer.median(), ee.Reducer.mean(), ee.Reducer.minMax(), ee.Reducer.stdDev(),
                   ee.Reducer.kurtosis(), ee.Reducer.skew()]
    ee_reducers = [ee.Reducer.median(), ee.Reducer.mean(), ee.Reducer.minMax()]

    newdict = {}
    for i in range(len(data)):

        dict2 = dict()

        # print(data.iloc[i]["Address"])
        # tic = time.perf_counter()

        if data.iloc[i]["Type"] == "ImageCollection":

            # Get the date range of images in the collection.
            collection = ee.ImageCollection(data.iloc[i]['Address'])
            time_range = collection.reduceColumns(ee.Reducer.minMax(), ["system:time_start"])

            try:
                min_time_range = time.strftime('%Y-%m', time.gmtime(ee.Date(time_range.get('min')).getInfo()['value'] / 1000.0))
                max_time_range = time.strftime('%Y-%m', time.gmtime(ee.Date(time_range.get('max')).getInfo()['value'] / 1000.0))

            except (requests.HTTPError, ee.EEException, ee.ee_exception.EEException, urllib3.exceptions.ProtocolError):
                min_time_range = '1900-01'
                max_time_range = '2100-12'

            if (min_time_range < time_frame[0] < max_time_range) & (min_time_range < time_frame[1] < max_time_range):
                pass
            elif min_time_range > time_frame[0]:
                time_frame[0] = min_time_range
                time_frame[1] = str(datetime.datetime.strptime(min_time_range, "%Y-%m").date() +
                                    datetime.timedelta(days=365.2425))
            elif max_time_range < time_frame[1]:
                time_frame[1] = max_time_range
                time_frame[0] = str(datetime.datetime.strptime(max_time_range, "%Y-%m").date() -
                                    datetime.timedelta(days=365.2425))

            image_coll_filtered = collection.filterDate(time_frame[0], time_frame[1]).filterBounds(rect)

            for ee_reducer in ee_reducers:

                # calculate median of all images in given time range and get image
                med_reduced_image = image_coll_filtered.reduce(ee_reducer)

                # Reduce the region. The region parameter is the Feature geometry.
                dict0 = med_reduced_image.reduceRegion(**{
                    'reducer': ee_reducer,
                    'geometry': rect,
                    'scale': 30,
                    'maxPixels': 1e9
                })

                try:
                    dict1 = dict(("{}@{}&timestamped".format(k, data.iloc[i]['Address']), v)
                                 for k, v in dict0.getInfo().items())

                except (requests.HTTPError, ee.EEException, ee.ee_exception.EEException, urllib3.exceptions.ProtocolError):
                    dict1 = dict()

                dict2.update(dict1)

        elif data.iloc[i]["Type"] == "Image":
            image = ee.Image(data.iloc[i]['Address'])

            for ee_reducer in ee_reducers:

                # Reduce the region. The region parameter is the Feature geometry.
                dict0 = image.reduceRegion(**{
                    'reducer': ee_reducer,
                    'geometry': rect,
                    'scale': 30,
                    'maxPixels': 1e9
                })
                try:
                    dict1 = dict(("{}@{}".format(k, data.iloc[i]['Address']), v)
                                 for k, v in dict0.getInfo().items())

                except (requests.HTTPError, ee.EEException, ee.ee_exception.EEException, urllib3.exceptions.ProtocolError):
                    dict1 = dict()

                dict2.update(dict1)
        # print(dict2)
        newdict.update(dict2)
        # toc = time.perf_counter()
        # print(f"Reading the value in {toc - tic:0.4f} seconds")

    geo_dict = geo_df_row.to_dict()
    geo_dict.update(newdict)

    return geo_dict
