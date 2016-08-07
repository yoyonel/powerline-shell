#!/usr/bin/env python
from __future__ import print_function
import os
import stat

try:
    import config
except ImportError:
    print('Created personal config.py for your customizations')
    import shutil

    shutil.copyfile('config.py.dist', 'config.py')
    import config

TEMPLATE_FILE = 'powerline_shell_base.py'
OUTPUT_FILE = 'powerline-shell.py'
SEGMENTS_DIR = 'segments'
THEMES_DIR = 'themes'


def load_source(srcfile):
    try:
        return ''.join(open(srcfile).readlines()) + '\n\n'
    except IOError:
        print('Could not open', srcfile)
        return ''


if __name__ == "__main__":
    source = load_source(TEMPLATE_FILE)
    source += load_source(os.path.join(THEMES_DIR, 'default.py'))

    if config.THEME != 'default':
        source += load_source(os.path.join(THEMES_DIR, config.THEME + '.py'))

    for segment in config.SEGMENTS:

        if isinstance(segment, list):
            segment_name, segment_pos = segment
            source += load_source(os.path.join(SEGMENTS_DIR, segment_name + '.py'))
            # assumes each segment file will have a function called
            # add_segment__[segment] that accepts the powerline object
            source += 'powerline.set_cur_position("{}")\n'.format(segment_pos)
            source += 'add_{}_segment(powerline)\n'.format(segment_name)
        else:
            source += load_source(os.path.join(SEGMENTS_DIR, segment + '.py'))
            # assumes each segment file will have a function called
            # add_segment__[segment] that accepts the powerline object
            source += 'powerline.set_cur_position("{}")\n'.format("left")
            source += 'add_{}_segment(powerline)\n'.format(segment)

    # source += 'sys.stdout.write(powerline.draw()[0])\n'
    source += 'segment_left, segment_right, segment_down = powerline.draw()\n'
    source += 'if powerline.pos_segment == "left":\n\tsys.stdout.write(segment_left)\n'
    source += 'elif powerline.pos_segment == "right":\n\tsys.stdout.write(segment_right)\n'
    source += 'elif powerline.pos_segment == "down":\n\tsys.stdout.write(segment_down)\n'

    try:
        open(OUTPUT_FILE, 'w').write(source)
        st = os.stat(OUTPUT_FILE)
        os.chmod(OUTPUT_FILE, st.st_mode | stat.S_IEXEC)
        print(OUTPUT_FILE, 'saved successfully')
    except IOError:
        print('ERROR: Could not write to powerline-shell.py. Make sure it is writable')
        exit(1)
