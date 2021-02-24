import unittest

from os import mkdir
import json
from os.path import join, exists
from shutil import rmtree

from unittest import mock

from backend import GPT_2_PATH, MODELS_DIR, CHECKPOINT_DIR, SAMPLES_DIR
from backend.api import rename_model
from backend.metadata import MODEL_METADATA_FILE
from backend.tests.api import ReqMock
from backend.tests.api.test_get_model_samples import create_sample
from backend.tests.test_metadata import create_metadata

TEST_MODEL = 'test_model'
TEST_CORE_MODEL = 'test_core_model'
TEST_MODEL_NEW = 'test_model_new'


class RenameTests(unittest.TestCase):
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
        samples_path = join(GPT_2_PATH, 'samples')
        test_model_path = join(path, TEST_MODEL)
        test_core_model_path = join(path, TEST_CORE_MODEL)
        test_model_new_path = join(path, TEST_MODEL_NEW)
        test_core_sample_path = join(samples_path, TEST_CORE_MODEL)
        test_new_sample_path = join(samples_path, TEST_MODEL_NEW)
        if exists(test_model_path):
            rmtree(test_model_path)

        if exists(test_core_model_path):
            rmtree(test_core_model_path)

        if exists(test_model_new_path):
            rmtree(test_model_new_path)

        if exists(test_core_sample_path):
            rmtree(test_core_sample_path)

        if exists(test_new_sample_path):
            rmtree(test_new_sample_path)

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
        rename_model(ReqMock('POST', {'id': TEST_CORE_MODEL, 'new_id': TEST_MODEL_NEW}))
        json_response, = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'success': True})
        self.assertFalse(exists(self.test_core_model_path))
        self.assertTrue(exists(join(MODELS_DIR, TEST_MODEL_NEW)))

    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_samples(self, json_mock):
        create_sample(TEST_CORE_MODEL, 5, 'rewrwerw')
        rename_model(ReqMock('POST', {'id': TEST_CORE_MODEL, 'new_id': TEST_MODEL_NEW}))
        json_response, = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'success': True})
        self.assertFalse(exists(self.test_core_model_path))
        self.assertTrue(exists(join(MODELS_DIR, TEST_MODEL_NEW)))
        self.assertFalse(exists(join(SAMPLES_DIR, TEST_CORE_MODEL)))
        self.assertTrue(exists(join(SAMPLES_DIR, TEST_MODEL_NEW)))

    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_history(self, json_mock):
        create_metadata(TEST_CORE_MODEL, {'history': [{'id': TEST_CORE_MODEL}]})
        rename_model(ReqMock('POST', {'id': TEST_CORE_MODEL, 'new_id': TEST_MODEL_NEW}))
        json_response, = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'success': True})
        self.assertFalse(exists(self.test_core_model_path))
        with open(join(MODELS_DIR, TEST_MODEL_NEW, MODEL_METADATA_FILE), 'r') as file:
            data = json.load(file)
            self.assertEqual(data.get('history')[0].get('id'), TEST_MODEL_NEW)

    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_no_checkpoint(self, json_mock):
        rmtree(CHECKPOINT_DIR)
        rename_model(ReqMock('POST', {'id': TEST_CORE_MODEL, 'new_id': TEST_MODEL_NEW}))
        json_response, = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'success': True})
        self.assertFalse(exists(self.test_core_model_path))
        self.assertTrue(exists(join(MODELS_DIR, TEST_MODEL_NEW)))

    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_checkpoint(self, json_mock):
        rename_model(ReqMock('POST', {'id': TEST_MODEL, 'new_id': TEST_MODEL_NEW}))
        json_response, = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'success': True})
        self.assertFalse(exists(self.test_model_path))
        self.assertTrue(exists(join(MODELS_DIR, TEST_MODEL_NEW)))

        self.assertFalse(exists(self.test_checkpoint_model_path))
        self.assertTrue(exists(join(CHECKPOINT_DIR, TEST_MODEL_NEW)))

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_taken(self, json_mock, *mocks):
        rename_model(ReqMock('POST', {'id': TEST_MODEL, 'new_id': TEST_CORE_MODEL}))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'New model name is taken'})
        self.assertEqual(code, 400)

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_not_existing(self, json_mock, *mocks):
        rename_model(ReqMock('POST', {'id': 'test', 'new_id': 'test2'}))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Model do not exists'})
        self.assertEqual(code, 400)

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_id_param(self, json_mock, *mocks):
        rename_model(ReqMock('POST', {'new_id': 'test2'}))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Param id is required'})
        self.assertEqual(code, 400)

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_new_id_param(self, json_mock, *mocks):
        rename_model(ReqMock('POST', {'id': 'test2'}))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Param new_id is required'})
        self.assertEqual(code, 400)


if __name__ == '__main__':
    unittest.main()
