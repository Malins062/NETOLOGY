import pytest
import requests
from read_data import load_testing_data

# Текстовый файл данныйх для тестирвания наличия папки на яндекс-диске
TEST_FILE = 'data/folders.json'
TOKEN = "AQAA...yBk"
URL = "https://cloud-api.yandex.net/v1/disk/resources"


class TestYandexRestAPI:

    @pytest.mark.parametrize('folder_name, expect_result', load_testing_data(TEST_FILE))
    def test_yandex_rest_api(self, folder_name, expect_result):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(TOKEN)
        }
        params = {"path": folder_name}
        assert requests.get(URL, headers=headers, params=params).status_code == expect_result
