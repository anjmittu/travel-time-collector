config = {
    'common': {
        'name': 'travel-time-collector-',
        'runtime': 'python3.7',
        'handler': 'handler.lambda_handler',
        'description': 'Collecting and storing travel times',
        'code-path': '../lambda',
        'timeout': 299,
        'memory': 1024
    },
    'to_work': {
        'profile': '',
        'role': '',
        'vpc': {},
        'env': {
            'Variables': {
                'google_key': "",
                'start_1': '',
                'end_1': '',
                'start_2': '',
                'end_2': '',
                "journey_type": "to_work"
            }
        }
    },
    'to_home': {
        'profile': '',
        'role': '',
        'vpc': {},
        'env': {
            'Variables': {
                'google_key': "",
                'start_1': '',
                'end_1': '',
                'start_2': '',
                'end_2': '',
                "journey_type": "to_home"
            }
        }
    }
}
