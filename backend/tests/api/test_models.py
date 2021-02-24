import unittest

from os import mkdir
import json
from os.path import join, exists
from shutil import rmtree

from unittest import mock

from backend import GPT_2_PATH, MODELS_DIR
from backend.api import get_models
from backend.metadata import MODEL_METADATA_FILE

TEST_MODEL = 'test_model'
TEST_CORE_MODEL = 'test_core_model'


class ModelsTests(unittest.TestCase):
    def setUp(self):
        if not exists(join(GPT_2_PATH, 'models')):
            mkdir(join(GPT_2_PATH, 'models'))
        self.tearDown()
        self.test_model_path = join(MODELS_DIR, TEST_MODEL)
        self.test_core_model_path = join(MODELS_DIR, TEST_CORE_MODEL)
        mkdir(self.test_model_path)
        mkdir(self.test_core_model_path)

        with open(join(self.test_model_path, MODEL_METADATA_FILE), "w") as metadata_file:
            json.dump({"core": False}, metadata_file)

    def tearDown(self):
        test_model_path = join(MODELS_DIR, TEST_MODEL)
        test_core_model_path = join(MODELS_DIR, TEST_CORE_MODEL)
        if exists(test_model_path):
            rmtree(test_model_path)

        if exists(test_core_model_path):
            rmtree(test_core_model_path)

    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_simple(self, json_mock, *mocks):
        get_models(None)
        json_response, = json_mock.call_args_list[0][0]
        self.assertTrue({'name': TEST_MODEL, 'core': False} in json_response)
        self.assertTrue({'name': TEST_CORE_MODEL, 'core': True} in json_response)


if __name__ == '__main__':
    unittest.main()
