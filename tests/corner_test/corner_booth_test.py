import pytest

from modules.corner_booth import CornerBooth

@pytest.mark.usefixtures('db_corner', 'app_corner')
class TestCornerBooth:

    def test_to_dict(self):
        booth = CornerBooth.create(booth_name='poor baby')
        print booth.to_dict()