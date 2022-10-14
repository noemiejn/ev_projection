import os

from osgeo import gdal

from ..helper import generate_output_file_tif, create_zip_shapefiles
from ..constant import CM_NAME
import pandas as pd
import numpy as np
import time

""" Entry point of the calculation module function"""

# TODO: CM provider must "change this code"
# TODO: CM provider must "not change input_raster_selection,output_raster  1 raster input => 1 raster output"
# TODO: CM provider can "add all the parameters he needs to run his CM
# TODO: CM provider can "return as many indicators as he wants"
def calculation(
    output_directory,
    inputs_raster_selection,
    inputs_vector_selection,
    inputs_parameter_selection,
):
    # TODO the folowing code must be changed by the code of the calculation module

    # generate the output raster file
    output_raster1 = generate_output_file_tif(output_directory)  # TBD
    # retrieve the inputs all input defined in the signature
    vehicles_per_habitant = float(inputs_parameter_selection["vehicles_per_habitant"])
    vehicle_rural_urban_factor = float(
        inputs_parameter_selection["vehicle_rural_urban_factor"]
    )
    year = int(inputs_parameter_selection["projection_year"])
    battery_capacity = float(inputs_parameter_selection["battery_capacity"])
    daily_traveled_diatance = float(
        inputs_parameter_selection["daily_traveled_diatance"]
    )
    fleet_renewal_share = float(inputs_parameter_selection["fleet_renewal_share"])

    # retrieve the inputs layes
    input_raster_selection = inputs_raster_selection["pop_tot_curr_density"]

    # retrieve the inputs layers
    # input_vector_selection = inputs_vector_selection["pop_tot_density_2018"]
    """
        print("inputs_vector_selection ",inputs_vector_selection)
        a_vehicle_stock =  inputs_vector_selection["a_vehicle_stock"]
        print("a_vehicle_stock ",a_vehicle_stock)
        b_final_energy_consumption =  inputs_vector_selection["b_final_energy_consumption"]
        print("b_final_energy_consumption ",b_final_energy_consumption)
        b_vehicle_stock =  inputs_vector_selection["b_vehicle_stock"]
        print("b_vehicle_stock ",b_vehicle_stock)
        bau_final_energy_consumption =  inputs_vector_selection["bau_final_energy_consumption"]
        print("bau_final_energy_consumption ",bau_final_energy_consumption)"""

    # TEST FOR VECTOR

    # In case of rater input
    ds = gdal.Open(input_raster_selection)
    ds_band = ds.GetRasterBand(1)

    # ----------------------------------------------------
    pixel_values_pop = ds.ReadAsArray()
    # ----------Reduction factor----------------
    b = 1 + vehicle_rural_urban_factor / 100
    a = 2 * vehicle_rural_urban_factor / 100 / np.ln(np.max(pixel_values_pop))
    car_density = (
        pixel_values_pop * vehicles_per_habitant * (b - a * np.ln(pixel_values_pop))
    )

    Share_electric_cars_new_registrations_2020 = 10
    yearly_factor = 0.01
    if year < 2035:
        for i in range(year - 2020):
            yearly_factor += fleet_renewal_share * (year - 2020) * (90 / 15)
    else:
        for i in range(13):
            yearly_factor += fleet_renewal_share * (2035 - 2020) * (90 / 15)
        for i in range(year - 2035):
            yearly_factor += fleet_renewal_share

    e_car_density = car_density * yearly_factor
    ev_sum = float(e_car_density.sum()) / 1000

    gtiff_driver = gdal.GetDriverByName("GTiff")
    # print ()
    out_ds = gtiff_driver.Create(
        output_raster1,
        ds_band.XSize,
        ds_band.YSize,
        1,
        gdal.GDT_UInt16,
        ["compress=DEFLATE", "TILED=YES", "TFW=YES", "ZLEVEL=9", "PREDICTOR=1"],
    )
    out_ds.SetProjection(ds.GetProjection())
    out_ds.SetGeoTransform(ds.GetGeoTransform())

    ct = gdal.ColorTable()
    ct.SetColorEntry(0, (0, 0, 0, 255))
    ct.SetColorEntry(1, (110, 220, 110, 255))
    out_ds.GetRasterBand(1).SetColorTable(ct)

    out_ds_band = out_ds.GetRasterBand(1)
    out_ds_band.SetNoDataValue(0)
    out_ds_band.WriteArray(e_car_density)

    del out_ds
    # output geneneration of the output
    graphics = []
    vector_layers = []

    # TODO to create zip from shapefile use create_zip_shapefiles from the helper before sending result
    # TODO exemple  output_shpapefile_zipped = create_zip_shapefiles(output_directory, output_shpapefile)
    result = dict()
    result["name"] = CM_NAME
    result["indicator"] = [
        {
            "unit": "Vehicles",
            "name": "Electric vehiscles in total in {}".format(year),
            "value": str(ev_sum),
        }
    ]
    result["graphics"] = graphics
    result["vector_layers"] = vector_layers
    result["raster_layers"] = [
        {
            "name": "layers of EV density in {}".format(year),
            "path": output_raster1,
            "type": "ev",
        }
    ]
    print("result", result)
    return result


def colorizeMyOutputRaster(out_ds):
    ct = gdal.ColorTable()
    ct.SetColorEntry(0, (0, 0, 0, 255))
    ct.SetColorEntry(1, (110, 220, 110, 255))
    out_ds.SetColorTable(ct)
    return out_ds
