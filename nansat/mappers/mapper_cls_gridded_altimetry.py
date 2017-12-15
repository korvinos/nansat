import os
from nansat.tools import WrongMapperError
from nansat.mappers.mapper_netcdf_cf import Mapper as MapperNetcdfCF

class Mapper(MapperNetcdfCF):
    def __init__(self, filename, gdal_dataset, gdal_metadata, *args, **kwargs):
        filebasename = os.path.basename(filename)
        if not (filebasename.startswith('dt_global_allsat_phy_l4_') and
                filebasename.endswith('nc')):
            raise WrongMapperError
        
        super(Mapper, self).__init__(filename, gdal_dataset, gdal_metadata, *args, **kwargs)

        self.dataset.SetMetadataItem('aaa', 'bbb')