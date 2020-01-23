#!/usr/bin/env python
"""
Oil budget (NOAA)
==================================
"""

from datetime import datetime
from opendrift.readers import reader_netCDF_CF_generic
from opendrift.models.openoil3D import OpenOil3D

# NOAA OilLibrary must be installed to run this example
o = OpenOil3D(loglevel=20, weathering_model='noaa')

# Using constand wind and current
#o.fallback_values['x_wind'] = 7
#o.fallback_values['x_sea_water_velocity'] = .7
#o.fallback_values['y_sea_water_velocity'] = .3
#o.fallback_values['land_binary_mask'] = 0

# Arome atmospheric model
reader_arome = reader_netCDF_CF_generic.Reader(o.test_data_folder() + '16Nov2015_NorKyst_z_surface/arome_subset_16Nov2015.nc')
# Norkyst ocean model
reader_norkyst = reader_netCDF_CF_generic.Reader(o.test_data_folder() + '16Nov2015_NorKyst_z_surface/norkyst800_subset_16Nov2015.nc')

o.add_reader([reader_arome, reader_norkyst])

# Seeding some particles
#oiltype='GULLFAKS, EXXON'
#oiltype='ALGERIAN CONDENSATE'
oiltype='MARTIN LINGE CRUDE 2016'
o.seed_elements(lon=4.88, lat=60.1, z=0, radius=3000, number=500,
                time=reader_norkyst.start_time, oiltype=oiltype)

# Adjusting some configuration
o.set_config('processes:dispersion', False)
o.set_config('processes:evaporation', True)
o.set_config('processes:emulsification', True)
o.set_config('processes:turbulentmixing', True)
o.set_config('turbulentmixing:timestep', 2)

# Running model (until end of driver data)
o.run(steps=4*24, time_step=900, time_step_output=3600)

# Print and plot results
#o.plot_oil_budget('oil_budget_MartinLingeCrude.png')
o.plot_oil_budget()
o.plot(fast=True)
o.animation(filename='oil_budget_noaa.gif', fast=True)

#%%
# .. image:: /gallery/animations/oil_budget_noaa.gif

o.plot_property('fraction_evaporated')
o.plot_property('density')
o.plot_property('water_fraction')
o.plot_property('viscosity')
o.plot_property('interfacial_area')
o.plot_property('z')