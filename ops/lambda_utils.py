import os
import boto3
from uuid import uuid4
from config import config
import zipfile as zf

def _get_client(service, env):
    region = 'us-east-1'
    return boto3.client(service, region_name=region)

def _lambda_exists(lambda_client, name):
    try:
        lambda_client.get_function(FunctionName=name)
        return True
    except:
        return False

def _zip_code(path):
    print('Zipping up package')
    print(path)
    zip_name = "lambda.zip"
    zip_handler = zf.ZipFile(zip_name, 'w', zf.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for f in files:
            path = os.path.join(root, f)
            zip_handler.write(path, path.split('/', 2)[2])
    for root, dirs, files in os.walk("../venv/lib/python3.7/site-packages/"):
        for f in files:
            path = os.path.join(root, f)
            zip_handler.write(path, path.split('/', 5)[5])
    zip_handler.close()
    return open(zip_name, 'rb').read()

def deploy_lambda(env):
    common = config['common']
    env_config = config[env]
    lambda_client = _get_client('lambda', env)
    lambda_name = common['name'] + env

    if _lambda_exists(lambda_client, lambda_name):
        print("Updating {} lambda in {}".format(lambda_name, env))
        lambda_client.update_function_configuration(
            FunctionName=lambda_name,
            Runtime=common['runtime'],
            Role=env_config['role'],
            Handler=common['handler'],
            Timeout=common['timeout'],
            MemorySize=common['memory'],
            VpcConfig=env_config['vpc'],
            Environment=env_config['env']
        )
        result = lambda_client.update_function_code(
            FunctionName=lambda_name,
            ZipFile=_zip_code(common['code-path'])
        )
        return result

    print("Creating {} lambda in {}".format(lambda_name, env))
    result = lambda_client.create_function(
        FunctionName=lambda_name,
        Runtime=common['runtime'],
        Role=env_config['role'],
        Handler=common['handler'],
        Code={'ZipFile':_zip_code(common['code-path'])},
        Description=common['description'],
        Timeout=common['timeout'],
        MemorySize=common['memory'],
        Publish=False,
        VpcConfig=env_config['vpc'],
        Environment=env_config['env']
    )
    return result
