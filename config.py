# This is the configuration file for your powerline-shell prompt
# Every time you make a change to this file, run install.py to apply changes
#
# For instructions on how to use the powerline-shell.py script, see the README

# Add, remove or rearrange these segments to customize what you see on the shell
# prompt. Any segment you add must be present in the segments/ directory

SEGMENTS = [
    # Set the terminal window title to user@host:dir
    'set_term_title',

    # Show current virtual environment (see http://www.virtualenv.org/)
    #    'virtual_env',

    # Show uptime
    #	'uptime',

    # Show time
    ['time', 'right'],

    # Show the current user's username as in ordinary prompts
    # ['username', 'left'],

    # Show the machine's hostname. Mostly used when ssh-ing into other machines
    'hostname',

    # Show a padlock when ssh-ing from another machine
    'ssh',

    # Show a padlock if the current user has no write access to the current
    # directory
    # 'read_only',

    # Show the current git branch and status
    ['git', 'left'],

    # Show the current mercurial branch and status
    #    'hg',

    # Show the current svn branch and status
    #    'svn',

    # Show the current fossil branch and status
    #    'fossil',

    # Show the last command's exit code if it was non-zero
    #    'exit_code',
    # ['docker', 'left'],
    ['docker_with_daemon', 'left'],

    ['ros', 'left'],
    ['ros_full', 'left'],
    # ['ros_logo', 'left'],

    #############################
    # Segment 'down'
    #############################
    # Show number of running jobs
    ['jobs', 'down'],

    # Show the current directory. If the path is too long, the middle part is
    # replaced with ellipsis ('...')
    ['cwd', 'down'],

    # Shows a '#' if the current user is root, '$' otherwise
    # Also, changes color if the last command exited with a non-zero error code
    ['root', 'down'],
    #############################
]

# Change the colors used to draw individual segments in your prompt
THEME = 'default'
# THEME = 'colortest.py'
# THEME = 'solarized-dark'