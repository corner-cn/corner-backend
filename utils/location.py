from geopy.geocoders import Nominatim

import logging
import sys

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

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


class GeoApi():

    def __init__(self, instance):
        self.redis = instance

    def geoadd(self, *args):
        return self._run('geoadd', *args)

    def georadius(self, *args):
        logger.info("running geo radius with args {}".format(args))
        return self._run('georadius', *args)

    def georadiusbymember(self, *args):
        return self._run('georadiusbymember', *args)

    def geoencode(self, *args):
        return self._run('geoadd', *args)

    def geodecode(self, *args):
        return self._run('geoadd', *args)

    def geodist(self, *args):
        return self._run('geodist', *args)

    def zrem(self, name, element):
        return self._run('zrem', name, element)

    def zrange(self, *args):
        return self._run('zrange', name, element)

    def zcard(self, name):
        return self._run('zcard', name)

    def _run(self, command, *args):
        return self.redis.execute_command('{} {}'.format(command, ' '.join(self._format_args(args))))

    def _format_args(self, args):
        return map(lambda x : str(x), args)
