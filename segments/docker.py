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
                'contents': u'\u1F433',
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
