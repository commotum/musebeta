import unittest

from os import mkdir
import json
from os.path import join, exists
from shutil import rmtree, copytree
from backend import GPT_2_PATH, MODELS_DIR, DATA_PATH

from backend.utils import MODEL_METADATA_FILE

from unittest import mock

from backend.api import generate_model
from backend.tests.api import ReqMock

TEST_MODEL = 'test_model'
TEST_CORE_MODEL = 'test_core_model'
TEST_MODEL_NEW = 'test_model_new'
TEST_MODEL_FILE = 'model-30.meta'


class GenerateTests(unittest.TestCase):
    def setUp(self):
        if not exists(join(GPT_2_PATH, 'models')):
            mkdir(join(GPT_2_PATH, 'models'))
        if not exists(join(GPT_2_PATH, 'checkpoint')):
            mkdir(join(GPT_2_PATH, 'checkpoint'))
        self.tearDown()
        test_model_path = join(DATA_PATH, TEST_MODEL)
        copytree(test_model_path, join(MODELS_DIR, TEST_MODEL))
        copytree(test_model_path, join(MODELS_DIR, TEST_CORE_MODEL))
        self.test_model_path = join(MODELS_DIR, TEST_MODEL)
        self.test_core_model_path = join(MODELS_DIR, TEST_CORE_MODEL)

        with open(join(self.test_model_path, MODEL_METADATA_FILE), "w") as metadata_file:
            json.dump({"core": False}, metadata_file)

    def tearDown(self):
        test_model_path = join(MODELS_DIR, TEST_MODEL)
        test_core_model_path = join(MODELS_DIR, TEST_CORE_MODEL)
        test_model_new_path = join(MODELS_DIR, TEST_MODEL_NEW)


        if exists(test_model_path):
            rmtree(test_model_path)

        if exists(test_core_model_path):
            rmtree(test_core_model_path)

        if exists(test_model_new_path):
            rmtree(test_model_new_path)

    # @mock.patch(
    #     "backend.utils.json_response", return_value=None
    # )
    # def test_simple(self, json_mock):
    #     generate_model(ReqMock('GET', {'id': TEST_MODEL, 'temperature': 1, 'top_k': 0, 'length': 20}))
    #     json_response, = json_mock.call_args_list[0][0]
    #     self.assertEqual(len(json_response) > 0, True)

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_not_existing(self, json_mock, *mocks):
        generate_model(ReqMock('GET', {'id': 'test'}))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Model do not exists'})
        self.assertEqual(code, 400)

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_id_param(self, json_mock, *mocks):
        generate_model(ReqMock('GET', {}))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Param id is required'})
        self.assertEqual(code, 400)


if __name__ == '__main__':
    unittest.main()
