import projects
from projects import paraview
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'test_include_labels:builderconfig': [
        'CATALYST',
        'PARAVIEWWEB',
    ],
    'test_excludes:builderconfig': [
        # TODO: Why are these disabled?
        'AnimatePipelineTime',
        'EyeDomeLighting',
        'UncertaintyRendering',
        'ProbePicking',
        'pvcs-tile-display',
    ],

    'configure_options:builderconfig': {
        'PARAVIEW_DATA_STORE:PATH': '/home/kitware/Dashboards/MyTests/ExternalData',
    },

    'slaveenv': {
        'DISPLAY': ':0',
        # since we're using mesa, no need to do offscreen screenshots.
        'PV_NO_OFFSCREEN_SCREENSHOTS': '1',
    },
}

buildsets = [
    {
        'os': 'linux',
        'libtype': 'static',
        'buildtype': 'release',
        'features': (
            'python',
            'mpi',
        ),
    },
    {
        'os': 'linux',
        'libtype': 'static',
        'buildtype': 'release',
        'category': 'exotic',
        'features': (
            'python',
            'mpi',
            'gui',
            'opengl2',
        ),
    },
    {
        'os': 'linux',
        'libtype': 'static',
        'buildtype': 'release',
        'features': (),
    },
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'debug',
        'category': 'exotic',
        'features': (
            'unified',
            'gui',
            'python',
            'mpi',
        ),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, paraview, buildsets, defprops)
