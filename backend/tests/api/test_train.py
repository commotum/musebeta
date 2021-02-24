import json
import unittest

from os import mkdir
from os.path import join, exists
from shutil import rmtree, copytree

from backend import GPT_2_PATH, MODELS_DIR, DATA_PATH
from backend.metadata import MODEL_METADATA_FILE
from backend.tests import data

from unittest import mock

from backend.api import train_model
from backend.tests.api import ReqMock

TEST_MODEL = 'test_model'
TEST_CORE_MODEL = 'test_core_model'
TEST_MODEL_NEW = 'test_model_new'


class TrainTests(unittest.TestCase):
    def setUp(self):
        if not exists(join(GPT_2_PATH, 'models')):
            mkdir(join(GPT_2_PATH, 'models'))
        self.tearDown()
        test_model_path = join(DATA_PATH, TEST_MODEL)
        copytree(test_model_path, join(MODELS_DIR, TEST_MODEL))
        self.test_model_path = join(MODELS_DIR, TEST_MODEL)

        with open(join(self.test_model_path, MODEL_METADATA_FILE), "w") as metadata_file:
            json.dump({"core": False}, metadata_file)

    def tearDown(self):
        path = join(GPT_2_PATH, 'models')
        checkpoint_path = join(GPT_2_PATH, 'checkpoint')
        test_model_path = join(path, TEST_MODEL)
        if exists(test_model_path):
            rmtree(test_model_path)

        if exists(checkpoint_path):
            test_checkpoint_model_path = join(checkpoint_path, TEST_MODEL)
            if exists(test_checkpoint_model_path):
                rmtree(test_checkpoint_model_path)

    # @mock.patch(
    #     "backend.utils.json_response", return_value=None
    # )
    # def test_simple(self, json_mock):
    #     train_model(ReqMock('POST', {'id': TEST_MODEL, 'every': 1, 'steps': 1}))
    #     json_response, = json_mock.call_args_list[0][0]
    #     self.assertEqual(json_response, {'success': True})
    #     with resources.path(gpt_2, '.') as path:
    #         self.assertTrue(exists(join(path, 'models', TEST_MODEL, MODEL_OUTPUT)))
    #         self.assertTrue(exists(join(path, 'samples', TEST_MODEL, 'samples-1')))

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_not_existing(self, json_mock, *mocks):
        train_model(ReqMock('POST', {'id': 'test', 'every': 1, 'steps': 1}))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Model do not exists'})
        self.assertEqual(code, 400)

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_id_param(self, json_mock, *mocks):
        train_model(ReqMock('POST', {'every': 1, 'steps': 1}))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Param id is required'})
        self.assertEqual(code, 400)

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_every_param(self, json_mock, *mocks):
        train_model(ReqMock('POST', {'id': 'test', 'steps': 1}))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Param every is required'})
        self.assertEqual(code, 400)

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_steps(self, json_mock, *mocks):
        train_model(ReqMock('POST', {'id': 'test', 'every': 1}))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Param steps is required'})
        self.assertEqual(code, 400)


if __name__ == '__main__':
    unittest.main()
