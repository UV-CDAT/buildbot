from buildbot.schedulers.basic import AnyBranchScheduler
from buildbot.changes import filter


from . import poll
import projects

__all__ = [
    'make_schedulers',
]


def make_schedulers(buildnames, secrets):
    codebases = projects.get_codebase(poll=poll, secrets=secrets)
    return [
        AnyBranchScheduler(
            name='SMTK Merge Request Scheduler',
            change_filter=filter.ChangeFilter(
                category='merge-request',
                project=poll.REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason='SMTK \'merge-request\' created/changed.',
            codebases=codebases,
            properties={
                'ctest_track': 'buildbot-smtk',
            },
        ),
        AnyBranchScheduler(
            name='SMTK Integration Branch Scheduler',
            change_filter=filter.ChangeFilter(
                category='integration-branch',
                project=poll.REPO),
            treeStableTimer=None,
            builderNames=buildnames,
            reason='SMTK \'master\' changed.',
            codebases=codebases,
            properties={
                'ctest_empty_binary_directory': True,
                'ctest_track': 'master',
            },
        ),
    ]
