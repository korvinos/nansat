#-------------------------------------------------------------------------------
# Name:        nansat_mapper_asar
# Purpose:     Mapping for Envisat ASAR-L1 data
#
# Author:      Knut-Frode
#
# Created:     13.12.2011
# Copyright:
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from vrt import VRT, Geolocation
from envisat import Envisat
import numpy as np

class Mapper(VRT, Envisat):
    ''' VRT with mapping of WKV for ASAR Level 1

        See Also
        --------
            http://envisat.esa.int/handbooks/asar/CNTR6-6-9.htm#eph.asar.asardf.asarrec.ASAR_Geo_Grid_ADSR
    '''

    def __init__(self, fileName, gdalDataset, gdalMetadata):

        product = gdalMetadata.get("MPH_PRODUCT", "Not_ASAR")

        if product[0:4] != "ASA_":
            raise AttributeError("ASAR_L1 BAD MAPPER")

        # Create VRTdataset with small VRTRawRasterbands
        incAngleDataset = self.create_VRT_with_rawbands(fileName, product[0:4], ["first_line_incidenceAngle"])

        # Enlarge the band to the underlying data band size
        self.incAngleDataset = incAngleDataset.resized(gdalDataset.RasterXSize, gdalDataset.RasterYSize)

        # create empty VRT dataset with geolocation only
        VRT.__init__(self, gdalDataset)

        # compute calibrated sigma0
        calibrationConst = gdalDataset.GetMetadataItem("MAIN_PROCESSING_PARAMS_ADS_1_CALIBRATION_FACTORS.1.EXT_CAL_FACT", "records")
        if calibrationConst is not None:
            rawCountsArray = np.uint32(gdalDataset.GetRasterBand(1).ReadAsArray())
            incAngleArray = self.incAngleDataset.dataset.GetRasterBand(1).ReadAsArray()
            sigma0Array = (rawCountsArray**2 * np.sin(incAngleArray * np.pi / 180.0)) / float(calibrationConst)
            # Create VRT for sigma0
            self.sigma0 = VRT(array=sigma0Array)
            metaDict = [{'source': self.sigma0.fileName, 'sourceBand': 1, 'wkv': 'surface_backwards_scattering_coefficient_of_radar_wave', 'parameters':{'band_name': 'sigma0', 'polarisation': gdalMetadata['SPH_MDS1_TX_RX_POLAR'], 'pass': gdalMetadata['SPH_PASS']}}]
        else:
            # Create a dictionary for ASAR band and geolocation
            metaDict = [{'source': fileName, 'sourceBand': 1, 'wkv': 'surface_backwards_scattering_coefficient_of_radar_wave', 'parameters':{'band_name': 'sigma0', 'polarisation': gdalMetadata['SPH_MDS1_TX_RX_POLAR'], 'pass': gdalMetadata['SPH_PASS'], 'warning': 'fake sigma0, not yet calibrated'}}]
            print "Could not get calibrated sigma0 because of no calibrationConst"

        #add dictionary for IncidenceAngle into metaDict
        for iBand in range(self.incAngleDataset.dataset.RasterCount):
            bandMetadata = self.incAngleDataset.dataset.GetRasterBand(iBand+1).GetMetadata()
            metaDict.append({'source': self.incAngleDataset.fileName, 'sourceBand': iBand+1, 'wkv': '', 'parameters':bandMetadata})

        # add bands with metadata and corresponding values to the empty VRT
        self._create_bands(metaDict)

        # set time
        self._set_envisat_time(gdalMetadata)

        ''' Set GeolocationArray '''
        #latlonName = {"latitude":"first_line_lats","longitude":"first_line_longs"}
        #self.add_geoarray_dataset(fileName, product[0:4], gdalDataset.RasterXSize, gdalDataset.RasterYSize, latlonName, gdalDataset.GetGCPProjection(), ["num_lines"])

