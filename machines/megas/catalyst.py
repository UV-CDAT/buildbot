import projects
from projects import catalyst
from kwextensions import factory
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'referencedir': '/home/kitware/dashboards/buildbot-share/paraview',
}

defconfig = {}

env = {
    'DISPLAY': ':1',
    'PATH': '/usr/lib64/mpich/bin:${PATH}',
}

buildsets = [
    {
        'os': 'linux',
        'features' : ('catalyst',),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, catalyst, buildsets,
    defprops=defprops,
    defconfig=defconfig,
    myfactory=factory.get_catalyst_buildfactory(),
    env=env
)
