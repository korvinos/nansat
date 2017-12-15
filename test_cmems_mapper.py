from nansat import Nansat

n = Nansat('/vagrant/shared/test_data/cls_gridded_altimetry/dt_global_allsat_phy_l4_20170515_20170914.nc')
print n
print n.time_coverage_start
print n.time_coverage_end
