Travel Time Collector

This is used to collect and compare the travel time between two sets of source
and destination.  The lambda just collects the data and writes it to s3.

## Deploy lambda

### Pre-reqs
You need to have aws credentials downloaded and stored in `~/.aws/credentials`.
You should also have python3 and pip installed.

### Download pip dependencies
You will need to download the dependencies for the lambda function, so that
they can be zipped up with the lambda.
```
$ cd ops
$ python -m venv ../venv
$ source ../venv/bin/activate
$ pip install boto3
$ pip install googlemaps
$ deactivate
```

### Create a config for deployment
In order for the deploy script to know where to deploy to, you need to add a config.py
file under the ops directory.  There is an example config given.

### Deploy to env given in config
When you deploy you need to give the name of an evn given in the config.  This lets
multiple env be stored in the config
```
$ python deploy_lambda_code.py to_work
$ python deploy_lambda_code.py to_home
```

## Set up trigger for lambda
The lambda can be set up to be triggered by any AWS lambda trigger.  A common
one might be to create a cloudwatch event that run every certain amount of time.
