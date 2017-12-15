import os
import json

import pythesint as pti

from nansat.tools import WrongMapperError
from nansat.mappers.mapper_netcdf_cf import Mapper as MapperNetcdfCF

class Mapper(MapperNetcdfCF):
    def __init__(self, filename, gdal_dataset, gdal_metadata, *args, **kwargs):
        filebasename = os.path.basename(filename)
        if not (filebasename.startswith('dt_global_allsat_phy_l4_') and
                filebasename.endswith('nc')):
            raise WrongMapperError
        
        super(Mapper, self).__init__(filename, gdal_dataset, gdal_metadata, *args, **kwargs)

        self.dataset.SetMetadataItem('platform',
            json.dumps(pti.get_gcmd_platform('Earth Observation Satellites')))


        self.dataset.SetMetadataItem('Data Center',
            json.dumps(dict(
                Bucket_Level0='GOVERNMENT AGENCIES-NON-US',
                Bucket_Level1='FRANCE',
                Bucket_Level2='',
                Bucket_Level3='',
                Short_Name='FR/CLS',
                Long_Name='COLLECTE LOCALISATION SATELLITES',
                Data_Center_URL='https://www.cls.fr/en/')))
