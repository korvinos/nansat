from nansat import Nansat

n = Nansat('/vagrant/shared/test_data/cls_gridded_altimetry/dt_global_allsat_phy_l4_20170515_20170914.nc')
print n
print n.mapper
print n.time_coverage_start
print n.time_coverage_end
print n.get_metadata('platform')
print n.get_metadata('Data Center')

print n.get_metadata('instrument')
print n.get_metadata('ISO Topic Category')

print n.get_metadata('Entry Title')
print n.get_metadata('Summary')
