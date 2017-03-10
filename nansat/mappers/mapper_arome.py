from dateutil.parser import parse

import json
import pythesint as pti

from nansat.mappers.mapper_netcdf_cf import Mapper as NetcdfCF
from nansat.tools import WrongMapperError

class Mapper(NetcdfCF):

    def __init__(self, *args, **kwargs):

        #fn = args[0] # filename
        #ds = args[1] # dataset
        mm = args[2] # metadata
        if not 'arome' in mm['NC_GLOBAL#source'].lower() and \
                not 'meps' in mm['NC_GLOBAL#source'].lower():
            raise WrongMapperError
    
        super(Mapper, self).__init__(*args, **kwargs)

        self.dataset.SetMetadataItem('time_coverage_start',
                (parse(mm['min_time'], fuzzy=True).isoformat()))
        self.dataset.SetMetadataItem('time_coverage_end',
                (parse(mm['max_time'], fuzzy=True).isoformat()))

        # Get dictionary describing the instrument and platform according to
        # the GCMD keywords
        mm = pti.get_gcmd_instrument('computer')
        ee = pti.get_gcmd_platform('models')

        self.dataset.SetMetadataItem('instrument', json.dumps(mm))
        self.dataset.SetMetadataItem('platform', json.dumps(ee))
