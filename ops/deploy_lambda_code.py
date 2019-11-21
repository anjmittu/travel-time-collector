import os
from sys import argv
import lambda_utils

def deploy_lambda_code(lambda_name, env):
    try:
        from config import config
    except:
        print("config can not be imported")
        return
    print("Deploying lambda to " + env)
    if env not in config[lambda_name]:
        print("The given environment does not exist")
        return
    os.environ['AWS_DEFAULT_PROFILE'] = config[lambda_name][env]['profile']
    arn = lambda_utils.deploy_lambda(lambda_name, env)['FunctionArn']

def main(lambda_name, env):
    deploy_lambda_code(lambda_name, env)

main(argv[1], argv[2])
