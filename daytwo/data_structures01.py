
pressure_readings_list = [3150,2780,3325,2890,3040,3180,2510,2815]

temp_readings_tup = (186,172,195,180,188,187,166,174)


sensor_active_set={True,False}

well_readings = {
    'pressure':pressure_readings_list,
    'temperature':temp_readings_tup,
    'sensor_active':sensor_active_set
}

"""print(pressure_readings_list, temp_readings_tup, sensor_active_set, well_readings)"""

#indexing
print(pressure_readings_list[0])

print(temp_readings_tup[-1])

print('the first five values of pressure readings are:', pressure_readings_list[0:5])

print('the well temperature readings are',well_readings['temperature'])

print('the well readings are:',well_readings)