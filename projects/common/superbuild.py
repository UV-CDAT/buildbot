import projects
from . import options

defaults = {
    'generator': 'Unix Makefiles',
    'buildflags': '-j1',

    'upload_file_patterns:project': [
        '*.tar.gz',
        '*.tgz',
    ],
}

os = projects.merge_config(options.os, {
    'windows': {
        'upload_file_patterns:project': [
            '*.zip',
            '*.exe',
        ],

        'generator': 'Ninja',
    },
    'osx': {
        'upload_file_patterns:project': [
            '*.dmg',
        ],

        'configure_options:project': {
            # CMake is picking make -i as default, which ends up ignoring errors and wasting time!
            'MAKE_COMMAND:STRING': '/usr/bin/make',
        },
    },
})
