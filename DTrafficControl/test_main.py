from DTrafficControl.iotawrapper import iotawrapper
from DTrafficControl.iotawrapper.iotawrapper import IOTAWrapper

iota = IOTAWrapper()
current_latitude = 21.0277644
current_longitude = 105.8341598

# traffics = iota.get_traffic_status_within(2.5, latitude=current_latitude, longitude=current_longitude)
# print(traffics)

spec_lat1, spec_lon1 = 21.019982, 105.847987
spec_lat2, spec_lon2 = 21.027934, 105.804151
spec_lat3, spec_lon3 = 21.017634, 105.844151

dis1 = iotawrapper.calculate_distance(_lat1=current_latitude,
                                      _lon1=current_longitude,
                                      _lat2=spec_lat2,
                                      _lon2=spec_lon2)
print(dis1)

iota.broadcast_traffic_status(latitude=spec_lat2, longitude=spec_lon2, traffic_status=iotawrapper.TRAFFIC_STATUS_LEV_0)
# iota.broadcast_traffic_status(latitude=spec_lat1, longitude=spec_lon1, traffic_status=iotawrapper.TRAFFIC_STATUS_LEV_2)
