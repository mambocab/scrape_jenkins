from collections import namedtuple
import jsonschema
import json
from util import pasteable_name


known_failure_schema = {
    'type': 'object',
    'properties': {
        'job_name': {'type': 'string'},
        'test_name': {'type': 'string'},
        'jira_url': {'type': 'string'},
        'known_pattern': {'type': 'string'}
    },
    'required': ['job_name', 'test_name', 'jira_url', 'known_pattern']
}
KnownFailure = namedtuple('KnownFailure', [p for p in known_failure_schema['properties']])


def validate_known_failure(d):
    jsonschema.validate(d, known_failure_schema)


def failure_from_dict(d):
    validate_known_failure(d)
    return KnownFailure(job_name=d['job_name'],
                        test_name=d['test_name'],
                        jira_url=d['jira_url'],
                        known_pattern=d['known_pattern'])


def get_known_failures(failures_file):
    with open(failures_file, 'r') as fp:
        data = json.load(fp)
    yield from (failure_from_dict(f) for f in data['known_failures'])


def failure_to_known_failure_json(failure, job_name):
    kf = {
        'job_name': job_name,
        'test_name': pasteable_name(failure),
        'jira_url': 'TKTKTK',
        'known_pattern': failure.errorDetails
    }
    validate_known_failure(kf)
    return json.dumps(kf, indent=4, separators=(',', ': '))
