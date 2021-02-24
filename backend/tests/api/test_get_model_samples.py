import json
import unittest

from os import mkdir
from os.path import join, exists
from shutil import rmtree
from backend import GPT_2_PATH

from unittest import mock

from backend.api import get_model_samples
from backend.tests.api import ReqMock

TEST_MODEL = 'test_model'


def create_sample(id: str, count: int, text: str):
    samples = join(GPT_2_PATH, 'samples')
    if not exists(samples):
        mkdir(samples)
    samples_path = join(samples, id)
    if not exists(samples_path):
        mkdir(samples_path)
    with open(join(samples_path, f"samples-{count}"), "w") as samples_file:
        samples_file.write(text)


def create_sample_metadata(id: str, count: int, loss: float, avg_loss: float):
    checkpoint = join(GPT_2_PATH, 'checkpoint')
    if not exists(checkpoint):
        mkdir(checkpoint)
    checkpoint_path = join(checkpoint, id)
    if not exists(checkpoint_path):
        mkdir(checkpoint_path)
    with open(join(checkpoint_path, f"metadata-{count}.json"), "w") as metadata_file:
        json.dump({'loss': loss, 'avg_loss': avg_loss}, metadata_file)


class SampleTests(unittest.TestCase):
    def setUp(self):
        if not exists(join(GPT_2_PATH, 'models')):
            mkdir(join(GPT_2_PATH, 'models'))
        samples_path = join(GPT_2_PATH, 'samples')
        if not exists(samples_path):
            mkdir(samples_path)
        self.tearDown()
        model_path = join(GPT_2_PATH, 'models', TEST_MODEL)
        if not exists(model_path):
            mkdir(model_path)
        self.model_samples = join(samples_path, TEST_MODEL)
        mkdir(self.model_samples)

    def tearDown(self):
        samples_path = join(GPT_2_PATH, 'samples')
        models_path = join(GPT_2_PATH, 'models')
        checkpoint_path = join(GPT_2_PATH, 'checkpoint')
        test_model_path = join(samples_path, TEST_MODEL)
        if exists(test_model_path):
            rmtree(test_model_path)

        test_model_path = join(models_path, TEST_MODEL)
        if exists(test_model_path):
            rmtree(test_model_path)

        test_model_path = join(checkpoint_path, TEST_MODEL)
        if exists(test_model_path):
            rmtree(test_model_path)

    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_simple(self, json_mock):
        sample = 'Sample'
        sample2 = 'Sample2'
        sample3 = 'Sample3'
        create_sample(TEST_MODEL, 5, sample)
        create_sample(TEST_MODEL, 15, sample2)
        create_sample(TEST_MODEL, 20, sample3)
        get_model_samples(ReqMock('GET', {'id': TEST_MODEL}))
        json_response, = json_mock.call_args_list[0][0]
        self.assertEqual(json_response.get('5'), {'data': [sample], 'loss': -1, 'avg_loss': -1})
        self.assertEqual(json_response.get('15'), {'data': [sample2], 'loss': -1, 'avg_loss': -1})
        self.assertEqual(json_response.get('20'), {'data': [sample3], 'loss': -1, 'avg_loss': -1})

    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_metadata(self, json_mock):
        sample = 'Sample'
        sample2 = 'Sample2'
        sample3 = 'Sample3'
        create_sample(TEST_MODEL, 5, sample)
        create_sample(TEST_MODEL, 15, sample2)
        create_sample(TEST_MODEL, 20, sample3)
        create_sample_metadata(TEST_MODEL, 5, 12.3, 32.1)
        create_sample_metadata(TEST_MODEL, 15, 14.3, 39.1)
        create_sample_metadata(TEST_MODEL, 20, 15.3, 36.1)
        get_model_samples(ReqMock('GET', {'id': TEST_MODEL}))
        json_response, = json_mock.call_args_list[0][0]
        self.assertEqual(json_response.get('5'), {'data': [sample], 'loss': 12.3, 'avg_loss': 32.1})
        self.assertEqual(json_response.get('15'), {'data': [sample2], 'loss': 14.3, 'avg_loss': 39.1})
        self.assertEqual(json_response.get('20'), {'data': [sample3], 'loss': 15.3, 'avg_loss': 36.1})

    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_samples(self, json_mock):
        sample = """======== SAMPLE 1 ========
Sample
======== SAMPLE 2 ========
Sample2"""
        create_sample(TEST_MODEL, 5, sample)
        get_model_samples(ReqMock('GET', {'id': TEST_MODEL}))
        json_response, = json_mock.call_args_list[0][0]
        self.assertEqual(json_response.get('5'), {'data': ['Sample\n', 'Sample2'], 'loss': -1, 'avg_loss': -1})

    @mock.patch(
        "backend.utils.json_response", return_value=None
    )
    def test_count(self, json_mock):
        sample = 'Sample'
        sample2 = 'Sample2'
        sample3 = 'Sample3'
        create_sample(TEST_MODEL, 5, sample)
        create_sample(TEST_MODEL, 15, sample2)
        create_sample(TEST_MODEL, 20, sample3)
        get_model_samples(ReqMock('GET', {'id': TEST_MODEL, 'amount': 15}))
        json_response, = json_mock.call_args_list[0][0]
        self.assertEqual(json_response.get('5'), {'data': [sample], 'loss': -1, 'avg_loss': -1})
        self.assertEqual(json_response.get('15'), {'data': [sample2], 'loss': -1, 'avg_loss': -1})
        self.assertEqual(json_response.get('20', None), None)

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_not_existing(self, json_mock, *mocks):
        get_model_samples(ReqMock('GET', {'id': 'test'}))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Model do not exists'})
        self.assertEqual(code, 400)

    @mock.patch(
        "backend.utils.error_json_response", return_value=None
    )
    def test_id_param(self, json_mock, *mocks):
        get_model_samples(ReqMock('GET', {}))
        json_response, code = json_mock.call_args_list[0][0]
        self.assertEqual(json_response, {'error': 'Param id is required'})
        self.assertEqual(code, 400)


if __name__ == '__main__':
    unittest.main()
