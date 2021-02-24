import unittest

from unittest import mock
from os import mkdir
import json
from os.path import join, exists
from shutil import rmtree

from backend import GPT_2_PATH, MODELS_DIR, CHECKPOINT_DIR
from backend.api import delete_model
from backend.tests.api import ReqMock
from backend.utils import MODEL_METADATA_FILE

TEST_MODEL = 'test_model'
TEST_CORE_MODEL = 'test_core_model'


class DeleteTests(unittest.TestCase):
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
        if exists(test_model_path):
            rmtree(test_model_path)

        if exists(test_core_model_path):
            rmtree(test_core_model_path)

        test_checkpoint_model_path = join(checkpoint_path, TEST_MODEL)
        if exists(test_checkpoint_model_path):
            rmtree(test_checkpoint_model_path)


    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_simple(self, json_mock):
        delete_model(ReqMock('DELETE', {'id': TEST_MODEL}))
        json_response, = json_mock.call_args_list[0][0]
        self.assertFalse(exists(self.test_model_path))
        self.assertEqual(json_response, {'success': True})


    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_samples(self, json_mock):
        if not exists(join(GPT_2_PATH, 'samples')):
            mkdir(join(GPT_2_PATH, 'samples'))
        mkdir(join(GPT_2_PATH, 'samples', TEST_MODEL))
        delete_model(ReqMock('DELETE', {'id': TEST_MODEL}))
        json_response, = json_mock.call_args_list[0][0]
        self.assertFalse(exists(join(GPT_2_PATH, 'samples', TEST_MODEL)))
        self.assertEqual(json_response, {'success': True})


    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_checkpoint(self, json_mock):
        delete_model(ReqMock('DELETE', {'id': TEST_MODEL}))
        json_response, = json_mock.call_args_list[0][0]
        self.assertFalse(exists(self.test_checkpoint_model_path))
        self.assertEqual(json_response, {'success': True})


    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_no_checkpoint(self, json_mock):
        rmtree(CHECKPOINT_DIR)
        delete_model(ReqMock('DELETE', {'id': TEST_MODEL}))
        json_response, = json_mock.call_args_list[0][0]
        self.assertFalse(exists(self.test_model_path))
        self.assertEqual(json_response, {'success': True})


    @mock.patch(
        "backend.utils.model_exists", return_value=False
    )
    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_not_existing(self, json_mock, *mocks):
        delete_model(ReqMock('DELETE', {'id': 'not_existing'}))

        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Model do not exists'})
        self.assertEqual(code, 400)


    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_id_param(self, json_mock, *mocks):
        delete_model(ReqMock('DELETE', {}))

        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Param id is required'})
        self.assertEqual(code, 400)


    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_core(self, json_mock, *mocks):
        delete_model(ReqMock('DELETE', {'id': TEST_CORE_MODEL}))
        json_response, status = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Core model deletion forbidden'})
        self.assertEqual(status, 403)


    if __name__ == '__main__':
        unittest.main()
