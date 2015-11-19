from util import indent, pasteable_name, matching_failures

base_url = 'http://cassci.datastax.com/'


def numberize(word, num):
    if num != 1:
        return {
            'failure': 'failures'
        }[word]
    else:
        return {
            'failure': 'failure'
        }[word]


def format_actual_failures(failure_dict, known_failures, verbosity):
    rv = ""
    for category in 'New Failures', 'Known Failures, Unknown Error', 'Known Failures':
        rv += indent(str(category), width=4) + '\n'
        category_failures = failure_dict[category]

        if verbosity > 1 or category != 'Known Failures':
            if category_failures:
                for f in category_failures:
                    rv += indent(pasteable_name(f).strip(), width=8) + '\n'

                    jira_urls = tuple('(see {})'.format(mf.jira_url)
                                      for mf in matching_failures(f, known_failures))
                    if jira_urls:
                        rv += indent('\n'.join(jira_urls), width=8) + '\n'
                    elif 'Known Failures' in category:
                        rv += indent('No known JIRA tickets. You should fix that ಠ_ಠ\n',
                                     width=8)

                    if verbosity > 2 or category != 'Known Failures':
                        rv += indent(f.errorDetails.strip(), width=12) + '\n'
            else:
                rv += indent('No failures in this category.', width=8) + '\n'
        else:
            n = len(category_failures)
            rv += indent('{n} {f} in this category'.format(n=n,
                                                           f=numberize('failure', n)),
                         width=8)

    return rv


def format_noise_failures(failure_dict, verbosity):
    rv = ""

    for category, category_failures in failure_dict.items():
        rv += indent(str(category), width=4) + '\n'

        if verbosity > 1:
            if category_failures:
                for f in category_failures:
                    rv += indent(pasteable_name(f).strip(), width=8) + '\n'
                    if verbosity > 2 or category != 'Known Failures':
                        rv += indent(f.errorDetails.strip(), width=12) + '\n'
            else:
                rv += indent('No failures in this category.', width=8) + '\n'
        else:
            n = len(category_failures)
            rv += indent('{n} {f} in this category'.format(n=n,
                                                           f=numberize('failure', n)),
                         width=8)

    return rv
