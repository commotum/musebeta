from os.path import join, exists
from os import listdir, rename, remove
import json
import re
from typing import Dict

from django.http import JsonResponse

from shutil import rmtree, copytree, copyfile

from backend import GPT_2_PATH, MODELS_DIR, CHECKPOINT_DIR
from backend.metadata import update_metadata, update_metadata_steps, handle_metadata, get_counter, MODEL_METADATA_FILE, \
    handle_checkpoint_metadata, rename_metadata, update_steps
from gpt_2.src.encode import encode, Args as EncodeArgs
from gpt_2.src.generate_samples import sample_model
from gpt_2.src.train import train, Args as TrainArgs

MODEL_OUTPUT = 'output.log'
MODEL_DATASET = 'dataset.npz'


def json_response(data):
    return JsonResponse(data, safe=False)


def error_json_response(data, status=500):
    return JsonResponse(data, safe=False, status=status)


def list_dir(path: str):
    return listdir(path)


def copy_dir(path: str, new_path: str):
    return copytree(path, new_path)


def copy_dir_content(path: str, new_path: str):
    for file_name in list_dir(path):
        file_path = join(path, file_name)
        new_file_path = join(new_path, file_name)
        if file_exists(new_file_path):
            delete_file(new_file_path)
        copyfile(file_path, new_file_path)


def file_exists(path: str):
    return exists(path)


def rename_file(path: str, new_path: str):
    return rename(path, new_path)


def get_file_json(path: str):
    with open(path) as metadata_raw:
        metadata = json.load(metadata_raw)
        return metadata


def delete_dir(path: str):
    if exists(path):
        rmtree(path)


def delete_file(path: str):
    if exists(path):
        remove(path)


def list_models():
    dir_list = list_dir(MODELS_DIR)
    ret = []
    for dir in dir_list:
        ret.append({'name': dir, **get_metadata(dir)})
    return ret


def get_model(id: str):
    return {'name': id, **get_metadata(id)}


def model_exists(id: str) -> bool:
    return file_exists(join(MODELS_DIR, id))


def get_metadata(id: str):
    metadata_path = join(MODELS_DIR, id, MODEL_METADATA_FILE)
    if not file_exists(metadata_path):
        return {'core': True}
    return get_file_json(metadata_path)


def rename_model(id: str, new_id: str) -> bool:
    path = join(GPT_2_PATH, 'models')
    checkpoint_path = join(GPT_2_PATH, 'checkpoint')
    samples_path = join(GPT_2_PATH, 'samples')
    dir_path = join(path, id)
    new_dir_path = join(path, new_id)
    rename_file(dir_path, new_dir_path)
    if exists(checkpoint_path):
        checkpoint = join(checkpoint_path, id)
        new_checkpoint = join(checkpoint_path, new_id)
        if file_exists(checkpoint):
            rename_file(checkpoint, new_checkpoint)

    if exists(samples_path):
        sample = join(samples_path, id)
        new_sample = join(samples_path, new_id)
        if file_exists(sample):
            rename_file(sample, new_sample)
    rename_metadata(new_id, new_id)

    return True


def delete_model(id: str) -> bool:
    model_path = join(GPT_2_PATH, 'models')
    checkpoint_path = join(GPT_2_PATH, 'checkpoint')
    samples_path = join(GPT_2_PATH, 'samples')
    delete_dir(join(model_path, id))
    delete_dir(join(checkpoint_path, id))
    delete_dir(join(samples_path, id))
    return True


def train_model(id: str, every: str, steps: str) -> bool:
    update_metadata(id, {"training": True})
    train(TrainArgs(
        {'dataset': join(GPT_2_PATH, 'models', id, MODEL_DATASET), 'sample_every': int(every), 'save_every': int(every),
         'steps_num': int(steps), 'model_name': id, 'run_name': id, 'output_file': MODEL_OUTPUT}))
    update_metadata(id, {"training": False})
    update_metadata_steps(id)
    return True


def encode_dataset(id: str, dataset: str) -> bool:
    txt_dataset = f"{MODEL_DATASET}.txt"
    with open(join(GPT_2_PATH, 'models', id, txt_dataset), "w") as dataset_file:
        dataset_file.write(dataset)
    encode(EncodeArgs({'model_name': id, 'in_text': join(GPT_2_PATH, 'models', id, txt_dataset),
                       'out_nzp': join(GPT_2_PATH, 'models', id, MODEL_DATASET)}))

    return True


def read_train_model(id: str, amount: int = 100) -> bool:
    ret = []
    with open(join(GPT_2_PATH, 'models', id, MODEL_OUTPUT), "r") as out:
        for line in (out.readlines()[-amount:]):
            ret.append(line.replace("\n", ""))
    return ret


def is_core_model(id: str) -> bool:
    return get_metadata(id).get('core')


def fork_model(id: str, new_id: str, dataset: str = None, file_name: str = None, amount: int = None) -> bool:
    path = join(GPT_2_PATH, 'models')
    checkpoint_path = join(GPT_2_PATH, 'checkpoint')
    dir_path = join(path, id)
    new_dir_path = join(path, new_id)
    copy_dir(dir_path, new_dir_path)
    checkpoint = join(checkpoint_path, id)
    if file_exists(checkpoint):
        files = list_dir(new_dir_path)
        for file in files:
            if re.search("^model.*$", file):
                delete_file(join(path, new_dir_path, file))
        copy_dir_content(checkpoint, join(path, new_id))
    counter = amount if amount else get_counter(id)
    if counter:
        files = list_dir(new_dir_path)
        for file in files:
            if "model-" in file and f"model-{counter}" not in file:
                delete_file(join(path, new_dir_path, file))
        handle_checkpoint_metadata(new_id, counter)
        update_steps(new_id, id, counter)
    files = list_dir(new_dir_path)
    for file in files:
        if re.search("^(events.*)|(counter)$", file):
            delete_file(join(path, new_dir_path, file))

    handle_metadata(new_id, id, file_name)

    if dataset:
        encode_dataset(new_id, dataset)

    return True


def generate_model(id: str, length: int, temp: float = 1.0, top_k: float = 0, input: str = None,
                   amount: int = None) -> str:
    generate_model_name = f"generate-{id}"
    if exists(join(GPT_2_PATH, 'models', generate_model_name)):
        delete_dir(join(GPT_2_PATH, 'models', generate_model_name))
    fork_model(id, generate_model_name, amount=amount)
    delete_file(join(GPT_2_PATH, 'models', generate_model_name, MODEL_OUTPUT))
    samples = sample_model(nsamples=1, input=input, model_name=generate_model_name, length=float(length),
                           temperature=float(temp),
                           top_k=float(top_k))

    sample = []
    for line in samples:
        if not re.search("^.*=+.*=+.*$", line):
            sample.append(line)
    delete_dir(join(GPT_2_PATH, 'models', generate_model_name))

    update_metadata_steps(id)
    return "".join(sample)


def get_model_samples(id: str, count: int = None) -> Dict:
    path = join(GPT_2_PATH, 'samples')
    if not exists(path):
        return {}
    samples_path = join(path, id)
    checkpoint_path = join(CHECKPOINT_DIR, id, )
    if not exists(samples_path):
        return {}

    ret = {}
    files = list_dir(samples_path)
    for file in files:
        *rest, number_str = file.split('-')
        if not count or int(number_str) <= int(count):
            ret[number_str] = {'data': [], 'loss': -1, 'avg_loss': -1}
            with open(join(samples_path, file), "r") as out:
                for line in out.readlines():
                    if re.search("^.*=+.*=+.*$", line):
                        ret[number_str]['data'].append("")
                    else:
                        if len(ret[number_str]['data']) == 0:
                            ret[number_str]['data'].append("")
                        ret[number_str]['data'][-1] += line
            if exists(checkpoint_path) and exists(join(checkpoint_path, f"metadata-{number_str}.json")):
                with open(join(checkpoint_path, f"metadata-{number_str}.json"), 'r') as metadata:
                    data = json.load(metadata)
                    ret[number_str]['loss'] = data.get('loss', -1)
                    ret[number_str]['avg_loss'] = data.get('avg_loss', -1)

    return ret
