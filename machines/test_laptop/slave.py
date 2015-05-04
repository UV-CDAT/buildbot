from buildbot.buildslave import BuildSlave

from machines import secrets

__all__ = [
    'SLAVE',
    'SLAVEPROPS',
]

SLAVE = BuildSlave('test-laptop', secrets.SECRETS['test-laptop']['password'],
    max_builds=1,
    properties={
        'cmakeroot': '/usr',
        'os': 'linux',
        'distribution': 'ubuntu-12.04',
    })

SLAVEPROPS = {
    'compiler': 'gcc-4.8.2',
    'generator:buildslave': 'Unix Makefiles',
    'maximum_parallel_level': 4,
    'configure_options:buildslave': {},
    'buildflags:buildslave': '-j4'
}
