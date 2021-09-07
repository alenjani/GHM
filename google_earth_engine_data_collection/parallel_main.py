from mpi4py import MPI

from GEE_2021_v5 import get_data_rapidly_new
from iteration_utilities import flatten
import pickle 
import json
import pandas as pd
import geopandas as gpd

version = MPI.Get_version()
# print("mpi version is ",version)

soft = MPI.INFO_ENV.get("soft")
# print(soft)
maxprocs=MPI.INFO_ENV.get("maxprocs")
# print(maxprocs)


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print("size is {}".format(size))

if rank == 0:

    googleearth_data = pd.read_csv("/home/users/alenjani/Jan2021_SatelliteImagery/Datasets_info_v1_short.csv")

    geo_df = gpd.read_file("/home/users/alenjani/Jan2021_SatelliteImagery/All_SHP_GEO/geo_df_0.shp")
    geo_df = geo_df.drop(columns=['geometry'])
    samples = range(len(geo_df))

    jobs = [samples[i::size] for i in range(size)]
else:
    jobs = None
    googleearth_data = None
    geo_df = None

# here you broadcast the variables that you only had in cpu rank=0. Scatter
jobs = comm.scatter(jobs, root=0)

googleearth_data = comm.bcast(googleearth_data, root=0)
geo_df = comm.bcast(geo_df, root=0)


sample_earth_info_dicts = []

for i in jobs:
    print(i)

    earth_info_dict = get_data_rapidly_new(googleearth_data, geo_df.iloc[i])
    #  print(earth_info_dict)
    sample_earth_info_dicts.append(earth_info_dict)

all_samples_earth_info_dicts = comm.gather(sample_earth_info_dicts, root=0)

if rank == 0:
    all_samples_earth_info_dicts = list(flatten(all_samples_earth_info_dicts))

    json.dump(all_samples_earth_info_dicts,
              open("/home/users/alenjani/Jan2021_SatelliteImagery/All_Google_Earth_Datasets/google_earth_df_0.txt", 'w'))

