import unittest

from os import mkdir
import json
from os.path import join, exists
from shutil import rmtree, copytree

from backend import CHECKPOINT_DIR, GPT_2_PATH, MODELS_DIR, DATA_PATH
from backend.metadata import MODEL_METADATA_FILE
from backend.tests import data
from backend.tests.data.utils import DATA_SET
from backend.tests.test_metadata import create_metadata

from backend.utils import MODEL_DATASET

from unittest import mock

from backend.api import fork_model
from backend.tests.api import ReqMock

TEST_MODEL = 'test_model'
TEST_CORE_MODEL = 'test_core_model'
TEST_MODEL_NEW = 'test new'
TEST_MODEL_FILE = 'model-30.meta'


def create_model_mock(id: str, count: int):
    checkpoint_path = join(CHECKPOINT_DIR, id)
    with open(join(checkpoint_path, f"model-{count}.meta"), "w") as file:
        file.write('')
    with open(join(checkpoint_path, f"model-{count}.data-00000-of-00001"), "w") as file:
        file.write('')
    with open(join(checkpoint_path, f"model-{count}.index"), "w") as file:
        file.write('')


class ForkTests(unittest.TestCase):
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

        self.test_checkpoint_model_path = join(CHECKPOINT_DIR, TEST_MODEL)
        mkdir(self.test_checkpoint_model_path)
        with open(join(self.test_checkpoint_model_path, TEST_MODEL_FILE), "w"):
            print('')
        with open(join(self.test_checkpoint_model_path, 'counter'), "w") as counter_file:
            counter_file.write('30\n')

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
        fork_model(ReqMock('POST', {'id': TEST_MODEL, 'new_id': TEST_MODEL_NEW}, DATA_SET))
        json_response, = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'success': True})
        self.assertTrue(exists(self.test_core_model_path))
        self.assertTrue(exists(join(MODELS_DIR, TEST_MODEL_NEW)))
        self.assertTrue(exists(join(MODELS_DIR, TEST_MODEL_NEW, MODEL_DATASET)))

    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_file_name(self, json_mock):
        file_name = 'test'
        fork_model(ReqMock('POST', {'id': TEST_MODEL, 'new_id': TEST_MODEL_NEW, 'fileName': file_name}, DATA_SET))
        json_response, = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'success': True})
        self.assertTrue(exists(self.test_core_model_path))
        with open(join(MODELS_DIR, TEST_MODEL_NEW, MODEL_METADATA_FILE), "r") as file:
            metadata = json.load(file)
            self.assertEqual(metadata.get('history')[0].get('file'), file_name)

    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_count(self, json_mock):
        create_model_mock(TEST_MODEL, 5)
        create_model_mock(TEST_MODEL, 15)
        create_model_mock(TEST_MODEL, 50)
        create_metadata(TEST_MODEL, {'history': [{'id': TEST_MODEL, 'steps': 50}, {'id': 'core'}]})
        fork_model(ReqMock('POST', {'id': TEST_MODEL, 'new_id': TEST_MODEL_NEW, 'count': 15}, DATA_SET))
        json_response, = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'success': True})
        self.assertTrue(exists(self.test_core_model_path))
        path = MODELS_DIR
        self.assertTrue(exists(join(path, TEST_MODEL_NEW)))
        self.assertTrue(exists(join(path, TEST_MODEL_NEW, 'model-15.meta')))
        self.assertTrue(exists(join(path, TEST_MODEL_NEW, 'model-15.index')))
        self.assertTrue(exists(join(path, TEST_MODEL_NEW, 'model-15.data-00000-of-00001')))
        self.assertFalse(exists(join(path, TEST_MODEL_NEW, 'model-30.meta')))
        self.assertFalse(exists(join(path, TEST_MODEL_NEW, 'model-5.meta')))
        with open(join(path, TEST_MODEL_NEW, MODEL_METADATA_FILE), 'r') as file:
            self.assertEqual(json.load(file).get('history')[1].get('steps'), 15)

    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_checkpoint_data(self, json_mock):
        create_model_mock(TEST_MODEL, 15)
        fork_model(ReqMock('POST', {'id': TEST_MODEL, 'new_id': TEST_MODEL_NEW, 'count': 15}, DATA_SET))
        json_response, = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'success': True})
        self.assertTrue(exists(self.test_core_model_path))
        with open(join(MODELS_DIR, TEST_MODEL_NEW, 'checkpoint'), 'r') as file:
            self.assertEqual(file.read(), """model_checkpoint_path: "model-15"
all_model_checkpoint_paths: "model-15"
""")

    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_no_checkpoint(self, json_mock):
        rmtree(CHECKPOINT_DIR)
        fork_model(ReqMock('POST', {'id': TEST_CORE_MODEL, 'new_id': TEST_MODEL_NEW}, DATA_SET))
        json_response, = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'success': True})
        self.assertTrue(exists(self.test_core_model_path))
        self.assertTrue(exists(join(MODELS_DIR, TEST_MODEL_NEW)))

    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_checkpoint(self, json_mock):
        fork_model(ReqMock('POST', {'id': TEST_MODEL, 'new_id': TEST_MODEL_NEW}, DATA_SET))
        json_response, = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'success': True})
        self.assertTrue(exists(self.test_model_path))
        self.assertTrue(exists(join(MODELS_DIR, TEST_MODEL_NEW)))
        self.assertTrue(exists(join(MODELS_DIR, TEST_MODEL_NEW, TEST_MODEL_FILE)))
        self.assertTrue(exists(self.test_checkpoint_model_path))

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_taken(self, json_mock, *mocks):
        fork_model(ReqMock('POST', {'id': TEST_MODEL, 'new_id': TEST_CORE_MODEL}, DATA_SET))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'New model name is taken'})
        self.assertEqual(code, 400)

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_no_dataset(self, json_mock, *mocks):
        fork_model(ReqMock('POST', {'id': 'test', 'new_id': 'test2'}))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Dataset not provided'})
        self.assertEqual(code, 400)

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_not_existing(self, json_mock, *mocks):
        fork_model(ReqMock('POST', {'id': 'test', 'new_id': 'test2'}, DATA_SET))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Model do not exists'})
        self.assertEqual(code, 400)

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_id_param(self, json_mock, *mocks):
        fork_model(ReqMock('POST', {'new_id': 'test2'}, DATA_SET))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Param id is required'})
        self.assertEqual(code, 400)

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_new_id_param(self, json_mock, *mocks):
        fork_model(ReqMock('POST', {'id': 'test2'}, DATA_SET))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Param new_id is required'})
        self.assertEqual(code, 400)


if __name__ == '__main__':
    unittest.main()
