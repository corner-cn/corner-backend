import pytest

from modules.corner_booth import CornerBooth

@pytest.mark.usefixtures('db_corner', 'app_corner')
class TestApi:

    def test_list_booth(self, app_corner):
        booth = CornerBooth.create_from_dict({"booth_name": "test"})
        client = app_corner.test_client()
        ret = client.get('v1/booth/{}'.format(booth.booth_id))
        print ret.data
        print ret.status
