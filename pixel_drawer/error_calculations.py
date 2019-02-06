import math

apparent_length = 20        # km
earth_radius = 6371         # km

radian = 2 * math.asin(apparent_length/2/earth_radius)
print(radian)
actual_length = radian * earth_radius
print(actual_length)
