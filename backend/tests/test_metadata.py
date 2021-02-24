import json
import unittest
from math import floor
from os import mkdir
from os.path import exists, join
from shutil import rmtree
from time import time, sleep

from backend import MODELS_DIR, CHECKPOINT_DIR, GPT_2_PATH
from backend.metadata import get_metadata, MODEL_METADATA_FILE, get_history_item, get_new_metadata, update_metadata, \
    handle_metadata, update_metadata_steps, COUNTER, get_counter, rename_metadata, update_steps

TEST_MODEL = 'test_model'


def create_metadata(id: str, data):
    metadata_path = join(MODELS_DIR, id, MODEL_METADATA_FILE)
    with open(metadata_path, "w") as metadata_file:
        json.dump(data, metadata_file)


def create_counter(id: str, amount: int):
    counter_path = join(CHECKPOINT_DIR, id, COUNTER)
    with open(counter_path, "w") as counter_file:
        counter_file.write(f"{amount}")


class MetadataCase(unittest.TestCase):
    def setUp(self):
        if not exists(join(GPT_2_PATH, 'models')):
            mkdir(join(GPT_2_PATH, 'models'))
        self.tearDown()
        self.test_model_path = join(MODELS_DIR, TEST_MODEL)
        mkdir(self.test_model_path)
        self.test_checkpoint_model_path = join(CHECKPOINT_DIR, TEST_MODEL)
        mkdir(self.test_checkpoint_model_path)

    def tearDown(self):
        test_model_path = join(MODELS_DIR, TEST_MODEL)
        if exists(test_model_path):
            rmtree(test_model_path)
        if exists(CHECKPOINT_DIR):
            test_checkpoint_model_path = join(CHECKPOINT_DIR, TEST_MODEL)
            if exists(test_checkpoint_model_path):
                rmtree(test_checkpoint_model_path)

    def test_get_metadata_not_existing(self, *mocks):
        metadata = get_metadata(TEST_MODEL)
        self.assertEqual(metadata, {})

    def test_get_metadata_existing(self, *mocks):
        test_metadata = {'core': False, 'random_prop': 'true'}
        create_metadata(TEST_MODEL, test_metadata)
        metadata = get_metadata(TEST_MODEL)
        self.assertEqual(metadata, test_metadata)

    def test_get_history_item(self, *mocks):
        current_time = floor(time())
        sleep(1)
        history_item = get_history_item(TEST_MODEL)
        self.assertEqual(history_item.get('id'), TEST_MODEL)
        self.assertGreater(history_item.get('created'), current_time)
        self.assertLess(history_item.get('created'), current_time + 3)
        self.assertEqual(history_item.get('file'), None)

    def test_get_history_item_file(self, *mocks):
        file = 'file'
        history_item = get_history_item(TEST_MODEL, file)
        self.assertEqual(history_item.get('file'), file)

    def test_get_new_metadata(self, *mocks):
        prev_id = 'prev_id'
        file = 'file'
        metadata = get_new_metadata(TEST_MODEL, prev_id, file)
        self.assertEqual(metadata.get('core'), False)
        self.assertEqual(metadata.get('training'), False)
        self.assertEqual(metadata.get('generating'), False)
        self.assertEqual(metadata.get('history'), [get_history_item(TEST_MODEL, file), get_history_item(prev_id)])

    def test_update_metadata_not_existing(self, *mocks):
        test_metadata = {'core': False, 'random_prop': 'true'}
        metadata = update_metadata(TEST_MODEL, test_metadata)
        self.assertEqual(metadata, test_metadata)
        self.assertEqual(get_metadata(TEST_MODEL), test_metadata)

    def test_update_metadata_existing(self, *mocks):
        test_metadata = {'core': False, 'random_prop': 'true'}
        update_test_metadata = {'random_prop': 'false', 'history': []}
        updated_metadata = {'core': False, 'random_prop': 'false', 'history': []}
        create_metadata(TEST_MODEL, test_metadata)
        metadata = update_metadata(TEST_MODEL, update_test_metadata)
        self.assertEqual(metadata, updated_metadata)
        self.assertEqual(get_metadata(TEST_MODEL), updated_metadata)

    def test_update_metadata_existing2(self, *mocks):
        test_metadata = {'core': False, 'random_prop': 'true', 'history': [{'data': 'someData'}]}
        update_test_metadata = {'random_prop': 'false'}
        updated_metadata = {'core': False, 'random_prop': 'false', 'history': [{'data': 'someData'}]}
        create_metadata(TEST_MODEL, test_metadata)
        metadata = update_metadata(TEST_MODEL, update_test_metadata)
        self.assertEqual(metadata, updated_metadata)
        self.assertEqual(get_metadata(TEST_MODEL), updated_metadata)

    def test_rename_metadata(self, *mocks):
        new_name = 'new_name'
        create_metadata(TEST_MODEL, {'history': [{'id': TEST_MODEL}]})
        metadata = rename_metadata(TEST_MODEL, new_name)
        self.assertEqual(metadata.get('history')[0].get('id'), new_name)
        self.assertEqual(get_metadata(TEST_MODEL).get('history')[0].get('id'), new_name)

    def test_update_steps(self, *mocks):
        create_metadata(TEST_MODEL, {'history': [{'id': TEST_MODEL, 'steps': 5}, {'id': 'id', 'steps': 60}]})
        metadata = update_steps(TEST_MODEL, TEST_MODEL, 15)
        self.assertEqual(metadata.get('history')[0].get('steps'), 15)
        self.assertEqual(metadata.get('history')[1].get('steps'), 60)

    def test_handle_metadata_not_existing(self, *mocks):
        prev_id = 'prev_id'
        file = 'file'
        metadata = handle_metadata(TEST_MODEL, prev_id, 'file')
        self.assertEqual(metadata, get_new_metadata(TEST_MODEL, prev_id, file))
        self.assertEqual(get_metadata(TEST_MODEL), get_new_metadata(TEST_MODEL, prev_id, file))

    def test_handle_metadata_existing(self, *mocks):
        prev_id = 'prev_id'
        file = 'file'
        history_item = get_history_item('test')
        test_metadata = {'core': False, 'random_prop': 'true', 'history': [history_item]}
        updated_metadata = {'core': False, 'training': False, 'generating': False, 'random_prop': 'true',
                            'history': [get_history_item(TEST_MODEL, file), history_item]}
        create_metadata(TEST_MODEL, test_metadata)
        metadata = handle_metadata(TEST_MODEL, prev_id, file)
        self.assertEqual(metadata, updated_metadata)
        self.assertEqual(get_metadata(TEST_MODEL), updated_metadata)

    def test_update_metadata_steps_not_existing(self, *mocks):
        metadata = update_metadata_steps(TEST_MODEL)
        self.assertEqual(metadata, None)
        self.assertEqual(get_metadata(TEST_MODEL), {})

    def test_get_counter(self, *mocks):
        amount = 10
        create_counter(TEST_MODEL, amount)
        counter = get_counter(TEST_MODEL)
        self.assertEqual(amount, counter)

    def test_update_metadata_steps(self, *mocks):
        amount = 10
        test_metadata = {'core': False, 'random_prop': 'true',
                         'history': [{'name': 'steps'}, {'name': 'test', 'steps': 3}, {'name': 'name'}]}
        updated_metadata = {'core': False, 'random_prop': 'true',
                            'history': [{'name': 'steps', 'steps': amount, 'updated': floor(time())},
                                        {'name': 'test', 'steps': 3},
                                        {'name': 'name'}]}
        create_metadata(TEST_MODEL, test_metadata)
        create_counter(TEST_MODEL, amount)
        metadata = update_metadata_steps(TEST_MODEL)
        self.assertEqual(metadata, updated_metadata)
        self.assertEqual(get_metadata(TEST_MODEL), updated_metadata)


if __name__ == '__main__':
    unittest.main()
