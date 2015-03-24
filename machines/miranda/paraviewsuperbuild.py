import projects
from projects import paraviewsuperbuild
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'upload_file_patterns:builderconfig': [ '*.zip', '*.exe' ],
    'generator': 'Ninja',
    'buildflags': '-l1',
    'test_excludes:builderconfig': [
        # Since server is MPI enabled, it needs to be run with MPI.
        # We'll fix that at some point.
        'PrintVersionServer',
    ],

    'configure_options:builderconfig': {
        'BUILD_TESTING:BOOL': 'ON',

        'USE_NONFREE_COMPONENTS:BOOL': 'ON',
        #'PARAVIEW_BUILD_WEB_DOCUMENTATION:BOOL': 'ON',

        # Superbuild Variables
        "ENABLE_acusolve:BOOL": "ON",
        "ENABLE_boost:BOOL": "ON",
        "ENABLE_cgns:BOOL": "ON",
        "ENABLE_matplotlib:BOOL": "ON",
        "ENABLE_mpi:BOOL": "ON",
        "ENABLE_numpy:BOOL": "ON",
        "ENABLE_paraview:BOOL": "ON",
        "ENABLE_qt:BOOL": "ON",
        "ENABLE_silo:BOOL": "ON",
        "ENABLE_visitbridge:BOOL": "ON",
        "ENABLE_vistrails:BOOL": "ON",
        "ENABLE_netcdf:BOOL": "ON",

        "7Z_EXE:FILEPATH": "C:/Program Files/7-Zip/7z.exe",

        # Location of the ftjam freetype build system executable
        "FTJAM_EXECUTABLE:FILEPATH": "C:/Tools/ftjam-2.5.2/jam.exe",

        # Use system qt
        "USE_SYSTEM_qt:BOOL": "ON",

        # Package the system qt files.
        "PACKAGE_SYSTEM_QT:BOOL": "ON",

        #Location where source tar-balls are (to be) downloaded.
        "download_location:PATH":"c:/bbd/superbuild-downloads",
    },

    'slaveenv': {
        'JSDUCK_HOME': 'C:/Tools/jsduck-4.4.1',
    },
}

#------------------------------------------------------------------------------
# VS9 (2008) 64-bit properties and environment.
#------------------------------------------------------------------------------
vs9x64props = {
    'compiler': 'msvc-2008-x64',
    'vcvarsall': 'C:\\Program Files (x86)\\Microsoft Visual Studio 9.0\\VC\\vcvarsall.bat',
    'vcvarsargument': 'amd64',

    'configure_options:builderconfig': {
        'QT_QMAKE_EXECUTABLE:FILEPATH': 'C:/Tools/qt-4.8.4/vs2008-x64/bin/qmake.exe',
    },

    'slaveenv': {
        'PATH': 'C:/Tools/jom;C:/Tools/qt-4.8.4/vs2008-x64/bin;${PATH}'
    },
}

#------------------------------------------------------------------------------
# VS9 (2008) 32-bit properties and environment.
#------------------------------------------------------------------------------
vs9x32props = {
    'compiler': 'msvc-2008-x86',
    'vcvarsall': 'C:\\Program Files (x86)\\Microsoft Visual Studio 9.0\\VC\\vcvarsall.bat',
    'vcvarsargument': 'x86',

    'configure_options:builderconfig': {
        'QT_QMAKE_EXECUTABLE:FILEPATH': 'C:/Tools/qt-4.8.4/vs2008-x32/bin/qmake.exe',
    },

    'slaveenv': {
        'PATH': 'C:/Tools/jom;C:/Tools/qt-4.8.4/vs2008-x32/bin;${PATH}'
    },
}

#------------------------------------------------------------------------------
buildsets = [
    {
        'os': 'windows',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': ('superbuild',),
    },
]

BUILDERS = projects.make_builders(slave.SLAVE, paraviewsuperbuild, buildsets,
    defprops=projects.merge_config(defprops, vs9x64props),
    dirlen=8
)

#------------------------------------------------------------------------------
buildsets = [
    {
        'os': 'windows',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': ('superbuild','32bit',),
    },
]

BUILDERS += projects.make_builders(slave.SLAVE, paraviewsuperbuild, buildsets,
    defprops=projects.merge_config(defprops, vs9x32props),
    dirlen=8)
