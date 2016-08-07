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

    def draw(self):
        text_left = (''.join(self.draw_segment(i) for i in range(len(self.segments)))
                     + self.reset) + ' '
        self.segments_width += len(self.segments) * 3  # for self.reset*len(self.segments) + ' '
        #
        text_right = (''.join(self.draw_right_segment(i) for i in reversed(range(len(self.segments_right))))
                      + self.reset) + ' '
        self.segments_right_width += len(self.segments_right) * 3  # for self.reset*len(self.segments_right) + ' '
        # self.segments_right_width = 21 + 3

        text_down = (''.join(self.draw_down_segment(i) for i in range(len(self.segments_down)))
                     + self.reset) + ' '

        total_widths = self.segments_width + \
                       self.segments_right_width

        spaces = max(0, int(self.width) - total_widths)
        fold = ' ' * spaces

        if len(self.segments_down) > 0:
            text = text_left + fold + text_right + \
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
    # arg_parser.add_argument('--pos_segment', action='store', default='left',
    #                         help='')
    #
    args = arg_parser.parse_args()

    # powerline = Powerline(args, get_valid_cwd(), width=args.width, pos_segment=args.pos_segment)
    powerline = Powerline(args, get_valid_cwd())


class DefaultColor:
    """
    This class should have the default colors for every segment.
    Please test every new segment with this theme first.
    """
    USERNAME_FG = 250
    USERNAME_BG = 240
    USERNAME_ROOT_BG = 124

    HOSTNAME_FG = 250
    HOSTNAME_BG = 238

    HOME_SPECIAL_DISPLAY = True
    HOME_BG = 31  # blueish
    HOME_FG = 15  # white
    PATH_BG = 237  # dark grey
    PATH_FG = 250  # light grey
    CWD_FG = 254  # nearly-white grey
    SEPARATOR_FG = 244

    READONLY_BG = 124
    READONLY_FG = 254

    SSH_BG = 166  # medium orange
    SSH_FG = 254

    REPO_CLEAN_BG = 148  # a light green color
    REPO_CLEAN_FG = 0  # black
    REPO_DIRTY_BG = 161  # pink/red
    REPO_DIRTY_FG = 15  # white

    JOBS_FG = 39
    JOBS_BG = 238

    CMD_PASSED_BG = 236
    CMD_PASSED_FG = 15
    CMD_FAILED_BG = 161
    CMD_FAILED_FG = 15

    SVN_CHANGES_BG = 148
    SVN_CHANGES_FG = 22  # dark green

    GIT_AHEAD_BG = 240
    GIT_AHEAD_FG = 250
    GIT_BEHIND_BG = 240
    GIT_BEHIND_FG = 250
    GIT_STAGED_BG = 22
    GIT_STAGED_FG = 15
    GIT_NOTSTAGED_BG = 130
    GIT_NOTSTAGED_FG = 15
    GIT_UNTRACKED_BG = 52
    GIT_UNTRACKED_FG = 15
    GIT_CONFLICTED_BG = 9
    GIT_CONFLICTED_FG = 15

    VIRTUAL_ENV_BG = 35  # a mid-tone green
    VIRTUAL_ENV_FG = 00

    # Colors for Docker segment
    # url: http://bitmote.com/index.php?post/2012/11/19/Using-ANSI-Color-Codes-to-Colorize-Your-Bash-Prompt-on-Linux
    DOCKER_BG = 32
    DOCKER_FG = 255
    DOCKER_RUNNING_FG = 40
    DOCKER_PAUSED_FG = 214
    DOCKER_EXITED_FG = 160
    DOCKER_RESTARTING_FG = 253


class Color(DefaultColor):
    """
    This subclass is required when the user chooses to use 'default' theme.
    Because the segments require a 'Color' class for every theme.
    """
    pass


def add_set_term_title_segment(powerline):
    term = os.getenv('TERM')
    if not (('xterm' in term) or ('rxvt' in term)):
        return

    if powerline.args.shell == 'bash':
        set_title = '\\[\\e]0;\\u@\\h: \\w\\a\\]'
    elif powerline.args.shell == 'zsh':
        set_title = '\033]0;%n@%m: %~\007'
    else:
        import socket
        set_title = '\033]0;%s@%s: %s\007' % (os.getenv('USER'), socket.gethostname().split('.')[0], powerline.cwd or os.getenv('PWD'))

    powerline.append(set_title, None, None, '')



powerline.set_cur_position("left")
add_set_term_title_segment(powerline)
def add_time_segment(powerline):
    if powerline.args.shell == 'bash':
        #time = ' \\t '
        # url: http://bneijt.nl/blog/post/add-a-timestamp-to-your-bash-prompt/
        time = ' \\D{%F %T} '
    elif powerline.args.shell == 'zsh':
        time = ' %* '
    else:
        import time
        time = ' %s ' % time.strftime('%H:%M:%S')

    powerline.append(time, Color.HOSTNAME_FG, Color.HOSTNAME_BG)


powerline.set_cur_position("left")
add_time_segment(powerline)
def add_hostname_segment(powerline):
    if powerline.args.colorize_hostname:
        from lib.color_compliment import stringToHashToColorAndOpposite
        from lib.colortrans import rgb2short
        from socket import gethostname
        hostname = gethostname()
        FG, BG = stringToHashToColorAndOpposite(hostname)
        FG, BG = (rgb2short(*color) for color in [FG, BG])
        host_prompt = ' %s ' % hostname.split('.')[0]

        powerline.append(host_prompt, FG, BG)
    else:
        if powerline.args.shell == 'bash':
            host_prompt = ' \\h '
        elif powerline.args.shell == 'zsh':
            host_prompt = ' %m '
        else:
            import socket
            host_prompt = ' %s ' % socket.gethostname().split('.')[0]

        powerline.append(host_prompt, Color.HOSTNAME_FG, Color.HOSTNAME_BG)


powerline.set_cur_position("left")
add_hostname_segment(powerline)
import re
import subprocess
import os

GIT_SYMBOLS = {
    'detached': u'\u2693',
    'ahead': u'\u2B06',
    'behind': u'\u2B07',
    'staged': u'\u2714',
    'notstaged': u'\u270E',
    'untracked': u'\u2753',
    'conflicted': u'\u273C'
}

def get_PATH():
    """Normally gets the PATH from the OS. This function exists to enable
    easily mocking the PATH in tests.
    """
    return os.getenv("PATH")

def git_subprocess_env():
    return {
        # LANG is specified to ensure git always uses a language we are expecting.
        # Otherwise we may be unable to parse the output.
        "LANG": "C",

        # https://github.com/milkbikis/powerline-shell/pull/126
        "HOME": os.getenv("HOME"),

        # https://github.com/milkbikis/powerline-shell/pull/153
        "PATH": get_PATH(),
    }


def parse_git_branch_info(status):
    info = re.search('^## (?P<local>\S+?)''(\.{3}(?P<remote>\S+?)( \[(ahead (?P<ahead>\d+)(, )?)?(behind (?P<behind>\d+))?\])?)?$', status[0])
    return info.groupdict() if info else None


def _get_git_detached_branch():
    p = subprocess.Popen(['git', 'describe', '--tags', '--always'],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         env=git_subprocess_env())
    detached_ref = p.communicate()[0].decode("utf-8").rstrip('\n')
    if p.returncode == 0:
        branch = u'{} {}'.format(GIT_SYMBOLS['detached'], detached_ref)
    else:
        branch = 'Big Bang'
    return branch


def parse_git_stats(status):
    stats = {'untracked': 0, 'notstaged': 0, 'staged': 0, 'conflicted': 0}
    for statusline in status[1:]:
        code = statusline[:2]
        if code == '??':
            stats['untracked'] += 1
        elif code in ('DD', 'AU', 'UD', 'UA', 'DU', 'AA', 'UU'):
            stats['conflicted'] += 1
        else:
            if code[1] != ' ':
                stats['notstaged'] += 1
            if code[0] != ' ':
                stats['staged'] += 1

    return stats


def _n_or_empty(_dict, _key):
    return _dict[_key] if int(_dict[_key]) > 1 else u''


def add_git_segment(powerline):
    try:
        p = subprocess.Popen(['git', 'status', '--porcelain', '-b'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             env=git_subprocess_env())
    except OSError:
        # Popen will throw an OSError if git is not found
        return

    pdata = p.communicate()
    if p.returncode != 0:
        return

    status = pdata[0].decode("utf-8").splitlines()

    branch_info = parse_git_branch_info(status)
    stats = parse_git_stats(status)
    dirty = (True if sum(stats.values()) > 0 else False)

    if branch_info:
        branch = branch_info['local']
    else:
        branch = _get_git_detached_branch()

    bg = Color.REPO_CLEAN_BG
    fg = Color.REPO_CLEAN_FG
    if dirty:
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG

    powerline.append(' %s ' % branch, fg, bg)
    # powerline.append_right(' %s ' % branch, fg, bg, separator=powerline.separator_right)

    def _add(_dict, _key, fg, bg):
        if _dict[_key]:
            _str = u' {}{} '.format(_n_or_empty(_dict, _key), GIT_SYMBOLS[_key])
            powerline.append(_str, fg, bg)
            # powerline.append_right(_str, fg, bg, separator=powerline.separator_right)

    if branch_info:
        _add(branch_info, 'ahead', Color.GIT_AHEAD_FG, Color.GIT_AHEAD_BG)
        _add(branch_info, 'behind', Color.GIT_BEHIND_FG, Color.GIT_BEHIND_BG)
    _add(stats, 'staged', Color.GIT_STAGED_FG, Color.GIT_STAGED_BG)
    _add(stats, 'notstaged', Color.GIT_NOTSTAGED_FG, Color.GIT_NOTSTAGED_BG)
    _add(stats, 'untracked', Color.GIT_UNTRACKED_FG, Color.GIT_UNTRACKED_BG)
    _add(stats, 'conflicted', Color.GIT_CONFLICTED_FG, Color.GIT_CONFLICTED_BG)


powerline.set_cur_position("left")
add_git_segment(powerline)
# vim:fileencoding=utf-8:noet
from powerline.segments import Segment, with_docstring
from requests.exceptions import ConnectionError
from docker import Client, tls


DOCKER_STATUSES = ('running', 'paused', 'exited', 'restarting')

SEGMENT_INFO = {
    'running': {
        # 'icon': '●',
        'icon': u'\u2022',
        # 'highlight_group': 'docker_running',
        'colors': [Color.DOCKER_RUNNING_FG, Color.DOCKER_BG]
    },
    'paused': {
        'icon': '~',
        # 'highlight_group': 'docker_paused',
        'colors': [Color.DOCKER_PAUSED_FG, Color.DOCKER_BG]
    },
    'exited': {
        # 'icon': '✖',
        'icon': u'\u00D7',
        # 'highlight_group': 'docker_exited',
        'colors': [Color.DOCKER_EXITED_FG, Color.DOCKER_BG]
    },
    'restarting': {
        # 'icon': '↻',
        'icon': u'\u21BB',
        # 'highlight_group': 'docker_restarting',
        'colors': [Color.DOCKER_RESTARTING_FG, Color.DOCKER_BG]
    }
}


class DockerSegment(Segment):
    def get_statuses_count(self):
        count = []
        for status in DOCKER_STATUSES:
            if status in self.ignore_statuses:
                continue
            containers = self.cli.containers(quiet=True, filters={'status': status})
            if not containers:
                continue
            count.append({'status': status, 'quantity': len(containers)})

        return count

    @staticmethod
    def build_segments(statuses_count):
        segments = [
            # {'contents': u'\U0001F433 ', 'highlight_groups': ['docker'], 'divider_highlight_group': 'docker:divider'}
            {
                'contents': u'\U0001F433 ',
                # 'highlight_groups': ['docker'],
                # 'divider_highlight_group': 'docker:divider',
                'colors': [Color.DOCKER_FG, Color.DOCKER_BG]
            }
        ]

        for count in statuses_count:
            segments.append({
                'contents': ' %s %d' % (SEGMENT_INFO[count['status']]['icon'], count['quantity']),
                # 'highlight_groups': [SEGMENT_INFO[count['status']]['highlight_group'], 'docker'],
                # 'divider_highlight_group': 'docker:divider',
                'colors': SEGMENT_INFO[count['status']]['colors']
            })

        return segments

    def __call__(self, pl, base_url='unix://var/run/docker.sock', use_tls=False, ca_cert=None, client_cert=None,
                 client_key=None, ignore_statuses=[]):
        # pl.debug('Running powerline-docker')

        self.pl = pl
        self.ignore_statuses = ignore_statuses
        tls_config = None

        if use_tls:
            tls_config = tls.TLSConfig(
                client_cert=(client_cert, client_key),
                verify=ca_cert
            )

        self.cli = Client(base_url=base_url, tls=tls_config)

        try:
            statuses = self.get_statuses_count()
        except ConnectionError:
            # pl.error('Cannot connect to Docker server on \'%s\'' % (base_url,))
            print('Cannot connect to Docker server on \'%s\'' % (base_url,))
            return
        except Exception as e:
            # pl.error(e)
            print(e)
            return

        return self.build_segments(statuses)


docker = with_docstring(DockerSegment(),
                        '''Return the status of Docker containers.

It will show the number of Docker containers running and exited.
It requires Docker and docker-py to be installed.

:param str base_url:
    base URL including protocol where your Docker daemon lives (e.g. ``tcp://192.168.99.109:2376``).
    Defaults to ``unix://var/run/docker.sock``, which is where it lives on most Unix systems.
:param list ignore_statuses:
    list of statuses which will be ignored and not printed out (e.g. ``["exited", "paused"]``).
:param bool use_tls:
    if True, it will enable TLS communication with the Docker daemon. Defaults to False.
:param str ca_cert:
    path to CA cert file (e.g. ``/home/user/.docker/machine/machines/default/ca.pem``)
:param str client_cert:
    path to client cert (e.g. ``/home/user/.docker/machine/machines/default/cert.pem``)
:param str client_key:
    path to client key (e.g. ``/home/user/.docker/machine/machines/default/key.pem``)


Divider highlight group used: ``docker:divider``.

Highlight groups used: ``docker_running``, ``docker_paused``, ``docker_exited``, ``docker_restarting``, ``docker``.
''')


def add_docker_segment(powerline):
    list_dict_segments = docker(None)

    for dict_segment in list_dict_segments:
        color_fg, color_bg = dict_segment['colors']
        powerline.append(dict_segment['contents'], color_fg, color_bg)
        # powerline.append_right(dict_segment['contents'], color_fg, color_bg, separator=powerline.separator_right)


powerline.set_cur_position("left")
add_docker_segment(powerline)
import os

ELLIPSIS = u'\u2026'


def replace_home_dir(cwd):
    home = os.getenv('HOME')
    if cwd.startswith(home):
        return '~' + cwd[len(home):]
    return cwd


def split_path_into_names(cwd):
    names = cwd.split(os.sep)

    if names[0] == '':
        names = names[1:]

    if not names[0]:
        return ['/']

    return names


def requires_special_home_display(name):
    """Returns true if the given directory name matches the home indicator and
    the chosen theme should use a special home indicator display."""
    return (name == '~' and Color.HOME_SPECIAL_DISPLAY)


def maybe_shorten_name(powerline, name):
    """If the user has asked for each directory name to be shortened, will
    return the name up to their specified length. Otherwise returns the full
    name."""
    if powerline.args.cwd_max_dir_size:
        return name[:powerline.args.cwd_max_dir_size]
    return name


def get_fg_bg(name):
    """Returns the foreground and background color to use for the given name.
    """
    if requires_special_home_display(name):
        return (Color.HOME_FG, Color.HOME_BG,)
    return (Color.PATH_FG, Color.PATH_BG,)


def add_cwd_segment(powerline):
    cwd = powerline.cwd or os.getenv('PWD')
    if not py3:
        cwd = cwd.decode("utf-8")
    cwd = replace_home_dir(cwd)

    if powerline.args.cwd_mode == 'plain':
        powerline.append(' %s ' % (cwd,), Color.CWD_FG, Color.PATH_BG)
        return

    names = split_path_into_names(cwd)

    max_depth = powerline.args.cwd_max_depth
    if max_depth <= 0:
        warn("Ignoring --cwd-max-depth argument since it's not greater than 0")
    elif len(names) > max_depth:
        # https://github.com/milkbikis/powerline-shell/issues/148
        # n_before is the number is the number of directories to put before the
        # ellipsis. So if you are at ~/a/b/c/d/e and max depth is 4, it will
        # show `~ a ... d e`.
        #
        # max_depth must be greater than n_before or else you end up repeating
        # parts of the path with the way the splicing is written below.
        n_before = 2 if max_depth > 2 else max_depth - 1
        names = names[:n_before] + [ELLIPSIS] + names[n_before - max_depth:]

    if (powerline.args.cwd_mode == 'dironly' or powerline.args.cwd_only):
        # The user has indicated they only want the current directory to be
        # displayed, so chop everything else off
        names = names[-1:]

    for i, name in enumerate(names):
        fg, bg = get_fg_bg(name)

        separator = powerline.separator_thin
        separator_fg = Color.SEPARATOR_FG
        is_last_dir = (i == len(names) - 1)
        if requires_special_home_display(name) or is_last_dir:
            separator = None
            separator_fg = None

        powerline.append(' %s ' % maybe_shorten_name(powerline, name), fg, bg,
                         separator, separator_fg)


powerline.set_cur_position("down")
add_cwd_segment(powerline)
def add_root_segment(powerline):
    root_indicators = {
        'bash': ' \\$ ',
        'zsh': ' %# ',
        'bare': ' $ ',
    }
    bg = Color.CMD_PASSED_BG
    fg = Color.CMD_PASSED_FG
    if powerline.args.prev_error != 0:
        fg = Color.CMD_FAILED_FG
        bg = Color.CMD_FAILED_BG
    powerline.append(root_indicators[powerline.args.shell], fg, bg)
    # powerline.append_down(root_indicators[powerline.args.shell], fg, bg)


powerline.set_cur_position("down")
add_root_segment(powerline)
sys.stdout.write(powerline.draw())
