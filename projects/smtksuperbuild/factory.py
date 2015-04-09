__all__ = [
    'get_factory',
    'get_source_steps'
]

from buildbot.process.factory import BuildFactory
from buildbot.process.properties import Property, Interpolate
from buildbot.steps.master import SetProperty
from buildbot.steps.source.git import Git
from buildbot.process import properties

from projects.smtk.factory import get_source_steps as get_smtk_source_steps
from projects.smtk import poll as smtk_poll

import projects
from . import poll

from kwextensions.steps import CTestDashboard,\
                               DownloadCommonCTestScript,\
                               DownloadCataystCTestScript,\
                               DownloadLauncher,\
                               CTestExtraOptionsDownload,\
                               SetCTestBuildNameProperty

@properties.renderer
def _extra(props):
    smtk_src_dir = '%s/source-smtk' % props.getProperty('builddir')
    smtk_src_dir = smtk_src_dir.replace('\\', '/')
    extra_options = [
        '-DSMTK_FROM_GIT:BOOL=OFF',
        '-DSMTK_FROM_SOURCE_DIR:BOOL=ON',
        '-DSMTK_SOURCE_DIR:PATH=%s' % smtk_src_dir,
    ]
    return '''
           # Extend the ctest_configure_options to pass options that set
           # the SMTK source dir for the Superbuild to use
           set (ctest_configure_options_extra "%s")
           set (ctest_configure_options "${ctest_configure_options};${ctest_configure_options_extra}")
           ''' % ';'.join(extra_options)

@properties.renderer
def _install_superbuild(props):
    do_install = props.getProperty('smtk_install_on_success', False)
    if not do_install:
        return ''

    make_install = props.hasProperty('developer_install_root')
    if make_install:
        make_install = '1'
    else:
        make_install = '0'
    install_root = props.getProperty('developer_install_root', '')
    return '''
           function (buildbot_post_all)
               if (NOT success OR NOT %s)
                   return ()
               endif ()

               set(smtk_install_root "%s")

               message("------- Installing developer mode build to: ${smtk_install_root}")

               # Start a new build so as not to mess with the existing output
               # results.
               ctest_start(Experimental)
               # Set the override and use a developer build.
               ctest_configure(
                   OPTIONS "-D__BUILDBOT_INSTALL_LOCATION:PATH=${smtk_install_root};-DENABLE_smtk_BUILD_MODE:STRING=Developer")
               # Do the build again.
               ctest_build()
               # Copy the developer config over.
               file(COPY        "${CTEST_BINARY_DIRECTORY}/smtk-Developer-Config.cmake"
                    DESTINATION "${smtk_install_root}")
           endfunction ()
           ''' % (make_install, install_root)

def get_source_steps(sourcedir='source'):
    codebase = projects.get_codebase_name(poll.REPO)
    update = Git(repourl=Interpolate('%%(src:%s:repository)s' % codebase),
        mode='incremental',
        method='clean',
        submodules=False,
        workdir=sourcedir,
        reference=Property('referencedir'),
        codebase=codebase,
        env={'GIT_SSL_NO_VERIFY': 'true'})

    steps = []
    steps.append(update)
    steps.append(SetProperty(name='SetSuperbuildSourceDir',
        property='sourcedir', value=sourcedir))
    return steps

def get_factory(buildset):
    '''Argument is the selected buildset. That could be used to build the
    factory as needed.'''
    factory = BuildFactory()

    codebases = [projects.get_codebase_name(poll.REPO),
                 projects.get_codebase_name(smtk_poll.REPO)]

    # Add steps to checkout SMTK codebase.
    for step in get_smtk_source_steps(sourcedir='source-smtk'):
        factory.addStep(step)

    # Add steps to checkout SMTKSuperbuild codebase.
    for step in get_source_steps():
        factory.addStep(step)

    factory.addStep(SetCTestBuildNameProperty(codebases=codebases))
    factory.addStep(DownloadCommonCTestScript())
    factory.addStep(CTestExtraOptionsDownload(
        s=Interpolate('%(kw:default)s%(kw:extra)s%(kw:installsuperbuild)s',
            default=CTestExtraOptionsDownload.DefaultRenderer,
            extra=_extra,
            installsuperbuild=_install_superbuild)))
    if buildset['os'] == 'windows':
        # DownloadLauncher is only needed for Windows.
        factory.addStep(DownloadLauncher())
    factory.addStep(
            SetProperty(property='ctest_dashboard_script',
                value=Interpolate('%(prop:builddir)s/common.ctest')))
    # We set a 2 hrs timeout since the smtk build step can take a while
    # without producing any output. When that happens, buildbot may kill the
    # process.
    factory.addStep(CTestDashboard(cdash_projectname=poll.CDASH_PROJECTNAME,
                                   timeout=60*60*2))
    return factory
