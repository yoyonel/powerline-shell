#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse
import os
import sys

# import unicodedata
# import re
# from wcwidth import wcswidth
# from ansicolor import strip_escapes
# import subprocess
py3 = sys.version_info.major == 3


def warn(msg):
    print('[powerline-bash] ', msg)


class Powerline:
    symbols = {
        'compatible': {
            'lock': 'RO',
            'network': 'SSH',
            #
            'separator': u'\u25B6',
            'separator_thin': u'\u276F',
            #
            'separator_right': u'\u25C0',
            'separator_right_thin': u'\u276E'
        },
        'patched': {
            'lock': u'\uE0A2',
            'network': u'\uE0A2',

            'separator': u'\uE0B0',
            'separator_thin': u'\uE0B1',
            #
            'separator_right': u'\u25C9',
            'separator_right_thin': u'\u2B83'
        },
        'flat': {
            'lock': '',
            'network': '',
            'separator': '',
            'separator_thin': '',
            #
            'separator_right': '',
            'separator_right_thin': ''
        },
    }

    color_templates = {
        'bash': '\\[\\e%s\\]',
        'zsh': '%%{%s%%}',
        'bare': '%s',
    }

    def __init__(self, _args, cwd, width=0, pos_segment="left"):
        self.args = _args
        self.cwd = cwd
        mode, shell = args.mode, args.shell
        self.color_template = self.color_templates[shell]
        self.reset = self.color_template % '[0m'
        self.lock = Powerline.symbols[mode]['lock']
        self.network = Powerline.symbols[mode]['network']
        #
        self.separator = Powerline.symbols[mode]['separator']
        self.separator_thin = Powerline.symbols[mode]['separator_thin']
        self.separator_right = Powerline.symbols[mode]['separator_right']
        self.separator_right_thin = Powerline.symbols[mode]['separator_right_thin']
        #
        self.segments = []
        self.segments_right = []
        self.segments_down = []
        #
        self.width = width
        self.segments_width = 0
        self.segments_right_width = 0
        self.segments_down_width = 0
        #
        self.pos_segment = pos_segment
        self.cur_position = "left"

    def set_cur_position(self, pos):
        self.cur_position = pos

    def color(self, prefix, code):
        if code is None:
            return ''
        else:
            return self.color_template % ('[%s;5;%sm' % (prefix, code))

    def fgcolor(self, code):
        return self.color('38', code)

    def bgcolor(self, code):
        return self.color('48', code)

    def append(self, content, fg, bg, separator=None, separator_fg=None):
        if self.cur_position == "right":
            self.append_right(content, fg, bg, separator, separator_fg)
        elif self.cur_position == "down":
            self.append_down(content, fg, bg, separator, separator_fg)
        else:
            self.append_left(content, fg, bg, separator, separator_fg)

    def append_left(self, content, fg, bg, separator=None, separator_fg=None):
        self.segments.append((content, fg, bg,
                              separator if separator is not None else self.separator,
                              separator_fg if separator_fg is not None else bg))
        self.segments_width += len(content.encode('utf-8'))
        # print("append_left - content:", '*' + content.encode('utf-8') + '*')

    def append_right(self, content, fg, bg, separator=None, separator_fg=None):
        self.segments_right.append((content, fg, bg,
                                    separator if separator is not None else self.separator,
                                    separator_fg if separator_fg is not None else bg))
        self.segments_right_width += len(content.encode('utf-8'))
        # print("append_right - content:", '*' + content.encode('utf-8') + '*')
        # print("append_right - content:", '/' + content + '\\')
        # print("append_right - len(content):", len(content))

    def append_down(self, content, fg, bg, separator=None, separator_fg=None):
        self.segments_down.append((content, fg, bg,
                                   separator if separator is not None else self.separator,
                                   separator_fg if separator_fg is not None else bg))
        self.segments_down_width += len(content)

    def draw_left_segments(self):
        return (''.join(self.draw_segment(i) for i in range(len(self.segments)))
                     + self.reset) + ' '

    def draw_right_segments(self):
        return (''.join(self.draw_right_segment(i) for i in range(len(self.segments_right)))
                     + self.reset) + ' '

    def draw_down_segments(self):
        return (''.join(self.draw_down_segment(i) for i in range(len(self.segments_down)))
                     + self.reset) + ' '

    def draw(self):
        text_left = self.draw_left_segments()
        text_right = self.draw_right_segments()
        text_down = self.draw_down_segments()

        # self.segments_width += len(self.segments) * 3  # for self.reset*len(self.segments) + ' '
        # self.segments_right_width += len(self.segments_right) * 3  # for self.reset*len(self.segments_right) + ' '
        # self.segments_right_width = 21 + 3
        # total_widths = self.segments_width + \
        #                self.segments_right_width
        # spaces = max(0, int(self.width) - total_widths)
        # fold = ' ' * spaces

        if len(self.segments_down) > 0:
            # text = text_left + fold + text_right + \
            #        '\n' + text_down + self.reset
            text = text_left + \
                   '\n' + text_down + self.reset
        else:
            text = text_left + self.reset

        # print("self.segments_width: ", self.segments_width)
        # print("self.segments_right_width: ", self.segments_right_width)
        # print("total_width: ", total_widths)

        # bashCommand = "echo {}".format(text_right.encode('utf-8'))
        # process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        # output = process.communicate()[0]
        # print("output: ", output)
        # print("len(output): ", len(output.decode('utf-8')))


        # print(wcswidth(text_right))
        # print(len(strip_escapes(text_right)))
        #
        # # \\[\\e%s\\]
        # # ('[%s;5;%sm' % (prefix, code))
        # # - prefix : [38, 48]
        # # \[\b[0-9]\{3\}\b;5;\b[0-9]\{3\}\bm
        # ansi_escape = re.compile(r'\\\[\\e\[[0-9]*;5;[0-9]*m\\\]')
        # sub_text_right = ansi_escape.sub('', text_right)
        # # sub_text_right = unicodedata.normalize('NFKD', sub_text_right).encode('ascii', 'ignore')
        # s_text_right = str(sub_text_right.encode('utf-8'))
        # for c in s_text_right:
        # print(c + " ")
        # print(len(s_text_right))
        # print(self.segments_right_width)

        if py3:
            return text
        else:
            return text.encode('utf-8')
            # return text_left.encode('utf-8'), \
            #        text_right.encode('utf-8'), \
            #        text_down.encode('utf-8')

    def draw_segment(self, idx):
        segment = self.segments[idx]
        next_segment = self.segments[idx + 1] if idx < len(self.segments) - 1 else None

        return ''.join((
            self.fgcolor(segment[1]),
            self.bgcolor(segment[2]),
            segment[0],
            self.bgcolor(next_segment[2]) if next_segment else self.reset,
            self.fgcolor(segment[4]),
            segment[3]))

    def draw_right_segment(self, idx):
        segment = self.segments_right[idx]
        next_segment = self.segments_right[idx + 1] if idx < len(self.segments_right) - 1 else None

        return ''.join((
            self.bgcolor(next_segment[2]) if next_segment else self.reset,
            self.fgcolor(segment[4]),
            segment[3],
            self.fgcolor(segment[1]),
            self.bgcolor(segment[2]),
            segment[0])
        )

    def draw_down_segment(self, idx):
        segment = self.segments_down[idx]
        next_segment = self.segments_down[idx + 1] if idx < len(self.segments_down) - 1 else None

        return ''.join((
            self.fgcolor(segment[1]),
            self.bgcolor(segment[2]),
            segment[0],
            self.bgcolor(next_segment[2]) if next_segment else self.reset,
            self.fgcolor(segment[4]),
            segment[3]))


def get_valid_cwd():
    """ We check if the current working directory is valid or not. Typically
        happens when you checkout a different branch on git that doesn't have
        this directory.
        We return the original cwd because the shell still considers that to be
        the working directory, so returning our guess will confuse people
    """
    # Prefer the PWD environment variable. Python's os.getcwd function follows
    # symbolic links, which is undesirable. But if PWD is not set then fall
    # back to this func
    try:
        cwd = os.getenv('PWD') or os.getcwd()
    except:
        warn("Your current directory is invalid. If you open a ticket at " +
             "https://github.com/milkbikis/powerline-shell/issues/new " +
             "we would love to help fix the issue.")
        sys.stdout.write("> ")
        sys.exit(1)

    parts = cwd.split(os.sep)
    up = cwd
    while parts and not os.path.exists(up):
        parts.pop()
        up = os.sep.join(parts)
    if cwd != up:
        warn("Your current directory is invalid. Lowest valid directory: "
             + up)
    return cwd


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--cwd-mode', action='store',
                            help='How to display the current directory', default='fancy',
                            choices=['fancy', 'plain', 'dironly'])
    arg_parser.add_argument('--cwd-only', action='store_true',
                            help='Deprecated. Use --cwd-mode=dironly')
    arg_parser.add_argument('--cwd-max-depth', action='store', type=int,
                            default=5, help='Maximum number of directories to show in path')
    arg_parser.add_argument('--cwd-max-dir-size', action='store', type=int,
                            help='Maximum number of letters displayed for each directory in the path')
    arg_parser.add_argument('--colorize-hostname', action='store_true',
                            help='Colorize the hostname based on a hash of itself.')
    arg_parser.add_argument('--mode', action='store', default='patched',
                            help='The characters used to make separators between segments',
                            choices=['patched', 'compatible', 'flat'])
    arg_parser.add_argument('--shell', action='store', default='bash',
                            help='Set this to your shell type', choices=['bash', 'zsh', 'bare'])
    arg_parser.add_argument('prev_error', nargs='?', type=int, default=0,
                            help='Error code returned by the last command')
    #
    # arg_parser.add_argument('--width', action='store', default=0,
    #                         help='')
    # arg_parser.add_argument('--chroot', action='store', default=0)
    # arg_parser.add_argument('--extra', action='store', default='')
    arg_parser.add_argument('--pos_segment', action='store', default='left',
                            help='')
    #
    args = arg_parser.parse_args()

    # powerline = Powerline(args, get_valid_cwd(), width=args.width, pos_segment=args.pos_segment)
    powerline = Powerline(args, get_valid_cwd())
