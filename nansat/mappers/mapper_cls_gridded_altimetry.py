from nansat.mappers.mapper_netcdf_cf import Mapper as MapperNetcdfCF

class Mapper(MapperNetcdfCF):
    def __init__(self, filename, gdal_dataset, gdal_metadata, *args, **kwargs):
        pass
