import projects
from projects import catalyst
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'referencedir': '/home/kitware/dashboards/buildbot-share/paraview',

    'slaveenv': {
        'DISPLAY': ':1',
        'PATH': '/usr/lib64/mpich/bin:${PATH}',
    },
}

defconfig = {}

buildsets = [
    {
        'os': 'linux',
        'buildtype': 'release',
        'features' : ('catalyst',),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, catalyst, buildsets,
    defprops=defprops,
    defconfig=defconfig
)
