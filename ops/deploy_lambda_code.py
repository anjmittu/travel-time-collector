import os
from sys import argv
import lambda_utils

def deploy_lambda_code(env):
    try:
        from config import config
    except:
        print("config can not be imported")
        return
    print("Deploying lambda to " + env)
    if env not in config:
        print("The given environment does not exist")
        return
    os.environ['AWS_DEFAULT_PROFILE'] = config[env]['profile']
    arn = lambda_utils.deploy_lambda(env)['FunctionArn']

def main(env):
    deploy_lambda_code(env)

main(argv[1])
