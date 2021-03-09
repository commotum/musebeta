import os
import logging
import boto3
from backend import GPT_2_PATH


logger = logging.getLogger(__file__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


s3 = boto3.resource('s3')
models_root = os.path.abspath(os.path.join(GPT_2_PATH, 'models'))
model_to_bucket_name_dict = {
    '124M': 'gpt2-model-124m',
}


def download_gpt2_models(model_name):
    logger.info(f'Download GPT-2 models: {model_name}')
    if model_name not in model_to_bucket_name_dict:
        logger.error(f'Unknown model {model_name}')
        return

    model_dir = os.path.join(models_root, model_name)
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    bucket = s3.Bucket(model_to_bucket_name_dict[model_name])

    for obj in bucket.objects.filter():
        target = os.path.join(model_dir, obj.key)
        if os.path.exists(target):
            logger.info(f'{target} already exists.')
        else:
            logger.info(f'Start downloading {target}.')
            bucket.download_file(obj.key, target)
            logger.info(f'{target} has been downloaded.')


if __name__ == '__main__':
    download_gpt2_models('124M')
