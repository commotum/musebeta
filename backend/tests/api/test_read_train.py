import unittest

from os import mkdir
from os.path import join, exists
from shutil import rmtree

from backend import GPT_2_PATH, MODELS_DIR
from backend.api import read_train_model

from backend.utils import MODEL_OUTPUT

from unittest import mock

from backend.tests.api import ReqMock

TEST_MODEL = 'test_model'
TEST_OUTPUT = '\n'.join([str(i) for i in range(0, 1000)])


class ReadTrainTests(unittest.TestCase):
    def setUp(self):
        if not exists(join(GPT_2_PATH, 'models')):
            mkdir(join(GPT_2_PATH, 'models'))
        self.tearDown()
        self.test_model_path = join(MODELS_DIR, TEST_MODEL)
        mkdir(self.test_model_path)

        with open(join(self.test_model_path, MODEL_OUTPUT), "w") as file:
            file.write(TEST_OUTPUT)

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

    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_simple(self, json_mock):
        read_train_model(ReqMock('GET', {'id': TEST_MODEL, 'amount': 10}))
        json_response, = json_mock.call_args_list[0][0]
        self.assertEqual(len(json_response), 10)
        self.assertEqual(json_response[-1], '999')
        self.assertEqual(json_response[-2], '998')

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_not_existing(self, json_mock, *mocks):
        read_train_model(ReqMock('GET', {'id': 'test'}))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Model do not exists'})
        self.assertEqual(code, 400)


if __name__ == '__main__':
    unittest.main()
