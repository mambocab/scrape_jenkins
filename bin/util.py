import os.path
from collections import namedtuple
import re
from urllib.parse import urljoin

PasteableComponents = namedtuple('PasteableComponents', ['file_name', 'class_name', 'test_case_name'])

def pastable_components(build):
    module_and_class_names = build.className.split('.')

    # this assumes that if a test class's path is foo_test.bar_test.TestFooBar,
    # it will be a class named TestFooBar in foo_test/bar_test.py
    *module_names, class_name = module_and_class_names
    file_name = os.path.join(*module_names) + '.py'
    test_case_name = build.name
    return PasteableComponents(file_name=file_name,
                               class_name=class_name,
                               test_case_name=test_case_name)


def indent(s, width=4, char=' '):
    i = width * char
    return '\n'.join([i + line for line in s.split('\n')])


def pasteable_name(build):
    components = pastable_components(build)
    return '{file_name}:{class_name}.{test_case_name}'.format(
        file_name=components.file_name,
        class_name=components.class_name,
        test_case_name=components.test_case_name
    )


def matching_failures(failure, known_failures):
    known_name_matches = [kf for kf in known_failures
                          if pasteable_name(failure) == kf.test_name]
    return [kf for kf in known_name_matches if
            re.search(kf.known_pattern, failure.errorDetails)]


def is_ok(result):
    return result.status in ('PASSED', 'SKIPPED', 'FIXED')


def result_url(base_url, job_name, build_number, result):
    module_and_class_names = result.className.split('.')

    # this assumes that if a test class's path is foo_test.bar_test.TestFooBar,
    # it will be a class named TestFooBar in foo_test/bar_test.py
    *module_names, class_name = module_and_class_names
    test_case_name = result.name

    return urljoin(base_url, 'job', job_name, build_number, 'testReport', 'junit',
                   '.'.join(list(module_names)), class_name, test_case_name)
