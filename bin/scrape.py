#!/usr/bin/env python3
import json
import os

from jenkinsapi.jenkins import Jenkins
from jenkinsapi.custom_exceptions import NoResults


JOB_NAME = 'cassandra-2.1_dtest'
RESULTS_DIR = os.path.join('data', JOB_NAME)
JENKINS_URL = 'http://cassci.datastax.com/'


def serialize_resultset(resultset):
    to_serialize = {k: v for (k, v) in resultset.__dict__.items()
                    if k != 'build'}
    return json.dumps(to_serialize)


def main():
    j = Jenkins(JENKINS_URL)
    job = j.get_job(JOB_NAME)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    for build_number in job.get_build_ids():
        results_file_name = os.path.join(os.path.abspath(RESULTS_DIR),
                                         str(build_number) + '.json')
        if os.path.exists(results_file_name):
            print('{} already written'.format(results_file_name))
            continue

        try:
            results = job.get_build(build_number).get_resultset()
        except NoResults:
            continue

        with open(results_file_name, 'w') as f:
            print('writing to {}'.format(results_file_name))
            print(serialize_resultset(results), file=f)


if __name__ == '__main__':
    _exported = main()
