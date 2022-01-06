import pytest
from datetime import datetime
from docs_storage import del_doc_shelf, search_value
from read_data import load_testing_data

# Текстовый файл данныйх для теста удаления документов из картотеки
TEST_FILE1 = 'data/del_doc_shelf.json'
TEST_FILE2 = 'data/search_value.json'


class TestDocumentsStorage:

    @classmethod
    def setup_class(cls):
        print(f'\n{datetime.now()} - начало ОБЩЕГО тестирования')

    def setup(self):
        print(f'\n{datetime.now()} - начало тестирования ФУНКЦИИ')

    @pytest.mark.parametrize('num_doc, expect_result', load_testing_data(TEST_FILE1))
    def test_delete_document(self, num_doc, expect_result):
        assert del_doc_shelf(num_doc) >= expect_result

    @pytest.mark.parametrize('lst, value, expect_result', load_testing_data(TEST_FILE2))
    def test_search_value(self, lst, value, expect_result):
        assert search_value(lst, value) == expect_result

    def teardown(self):
        print(f'\n{datetime.now()} - окончание тестирования ФУНКЦИИ')

    @classmethod
    def teardown_class(cls):
        print(f'\n{datetime.now()} - окончание ОБЩЕГО тестирования')
