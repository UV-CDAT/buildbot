import projects
from projects import paraviewsuperbuild
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'upload_file_patterns:builderconfig': [
        '*.tar.gz',
        '*.tgz',
    ],

    'slaveenv': {
        'DISPLAY': ':0',
        # since we're using mesa, no need to do offscreen screenshots.
        'PV_NO_OFFSCREEN_SCREENSHOTS': '1',
    },
}

defconfig = {
    'BUILD_TESTING:BOOL': 'ON',

    'USE_NONFREE_COMPONENTS:BOOL': 'ON',
    'PARAVIEW_BUILD_WEB_DOCUMENTATION:BOOL': 'ON',

    'ENABLE_acusolve:BOOL': 'ON',
    'ENABLE_boost:BOOL': 'ON',
    'ENABLE_cgns:BOOL': 'ON',
    'ENABLE_cosmotools:BOOL': 'ON',
    'ENABLE_ffmpeg:BOOL': 'ON',
    'ENABLE_manta:BOOL': 'ON',
    'ENABLE_matplotlib:BOOL': 'ON',
    'ENABLE_mpi:BOOL': 'ON',
    'ENABLE_nektarreader:BOOL': 'ON',
    'ENABLE_numpy:BOOL': 'ON',
    'ENABLE_paraview:BOOL': 'ON',
    'ENABLE_python:BOOL': 'ON',
    'ENABLE_qt:BOOL': 'ON',
    'ENABLE_silo:BOOL': 'ON',
    'ENABLE_visitbridge:BOOL': 'ON',
    'ENABLE_vistrails:BOOL': 'ON',

    'download_location:PATH': '/home/kitware/Dashboards/MyTests/ParaViewSuperbuild-downloads',
}

buildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': ('superbuild',),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, paraviewsuperbuild, buildsets,
    defprops=defprops,
    defconfig=defconfig
)
