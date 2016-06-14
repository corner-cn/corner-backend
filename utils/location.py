from geopy.geocoders import Nominatim


def get_reverse(latitude, longitude):
    geolocator = Nominatim()
    location = geolocator.reverse("39.93244700173409, 116.44803521224406".format(latitude, longitude))
    if location:
        location_address_tuple = location.address.split(",")
        country = location_address_tuple[-1]
        city = location_address_tuple[-3]
        district = location_address_tuple[-4]

        return [country, city, district]
    else:
        return None
