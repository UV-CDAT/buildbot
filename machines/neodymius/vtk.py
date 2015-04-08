import projects
from projects import vtk
from . import slave

__all__ = [
    'BUILDERS',
]

defprops = {
    'configure_options:builderconfig': {
        'VTK_DATA_STORE:PATH': '/home/kitware/Dashboards/ExternalData/vtk',

        'OPENGL_INCLUDE_DIR:PATH': '/opt/mesa/include',
        'OPENGL_gl_LIBRARY:FILEPATH': '/opt/mesa/lib/libGL.so',
        'OPENGL_glu_LIBRARY:FILEPATH': '',
    },

    'slaveenv': {
        'DISPLAY': ':0',
    },
}

iccprops = projects.merge_config(defprops, {
    'compiler': 'icc-14.0.0',

    'configure_options:builderconfig': {
        'VTK_BUILD_ALL_MODULES:BOOL': 'ON',
        'VTK_BUILD_ALL_MODULES_FOR_TESTS:BOOL': 'ON',
    },
    'test_excludes:builderconfig': [
        # These two tests fail with no output and an exit value of 1.
        # Excluding until someone has time to look at them so that dashboard
        # will be green.
        'vtkRenderingTkPython-TestTkRenderWindowInteractor',
        'vtkRenderingTkPython-TestTkRenderWidget',
        # This test is flaky and no time at the moment to debug it.
        'vtkInteractionWidgetsCxx-TestImageActorContourWidget',
    ],
})

iccbuildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'python',
            'icc',
        ),
    },
]

BUILDERS = projects.make_builders(slave, vtk, iccbuildsets, iccprops)

gccbuildsets = [
    {
        'os': 'linux',
        'libtype': 'shared',
        'buildtype': 'release',
        'features': (
            'python',
        ),
    },
]

BUILDERS += projects.make_builders(slave, vtk, gccbuildsets, defprops)
