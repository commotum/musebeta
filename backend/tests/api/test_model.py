import unittest

from os import mkdir
import json
from os.path import join, exists
from shutil import rmtree

from unittest import mock

from backend import GPT_2_PATH, MODELS_DIR, CHECKPOINT_DIR
from backend.api import get_model
from backend.metadata import MODEL_METADATA_FILE
from backend.tests.api import ReqMock

TEST_MODEL = 'test_model'
TEST_CORE_MODEL = 'test_core_model'
TEST_MODEL_NEW = 'test_model_new'


class ModelTests(unittest.TestCase):
    def setUp(self):
        if not exists(join(GPT_2_PATH, 'models')):
            mkdir(join(GPT_2_PATH, 'models'))
        if not exists(join(GPT_2_PATH, 'checkpoint')):
            mkdir(join(GPT_2_PATH, 'checkpoint'))
        self.tearDown()
        self.test_model_path = join(MODELS_DIR, TEST_MODEL)
        self.test_core_model_path = join(MODELS_DIR, TEST_CORE_MODEL)
        mkdir(self.test_model_path)
        mkdir(self.test_core_model_path)

        with open(join(self.test_model_path, MODEL_METADATA_FILE), "w") as metadata_file:
            json.dump({"core": False}, metadata_file)

        self.test_checkpoint_model_path = join(CHECKPOINT_DIR, TEST_MODEL)
        mkdir(self.test_checkpoint_model_path)

    def tearDown(self):
        path = join(GPT_2_PATH, 'models')
        checkpoint_path = join(GPT_2_PATH, 'checkpoint')
        test_model_path = join(path, TEST_MODEL)
        test_core_model_path = join(path, TEST_CORE_MODEL)
        test_model_new_path = join(path, TEST_MODEL_NEW)
        if exists(test_model_path):
            rmtree(test_model_path)

        if exists(test_core_model_path):
            rmtree(test_core_model_path)

        if exists(test_model_new_path):
            rmtree(test_model_new_path)

        if exists(checkpoint_path):
            test_checkpoint_model_path = join(checkpoint_path, TEST_MODEL)
            test_checkpoint_model_path_new = join(checkpoint_path, TEST_MODEL_NEW)
            if exists(test_checkpoint_model_path):
                rmtree(test_checkpoint_model_path)
            if exists(test_checkpoint_model_path_new):
                rmtree(test_checkpoint_model_path_new)

    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_simple(self, json_mock):
        get_model(ReqMock('GET', {'id': TEST_CORE_MODEL}))
        json_response, = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {"name": TEST_CORE_MODEL, 'core': True})

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_not_existing(self, json_mock, *mocks):
        get_model(ReqMock('GET', {'id': 'test', 'new_id': 'test2'}))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Model do not exists'})
        self.assertEqual(code, 400)

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_id_param(self, json_mock, *mocks):
        get_model(ReqMock('GET', {'new_id': 'test2'}))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Param id is required'})
        self.assertEqual(code, 400)


if __name__ == '__main__':
    unittest.main()
