# vim:fileencoding=utf-8:noet
from powerline.segments import Segment, with_docstring
import subprocess
import os

ROS_STATUSES = ('running')

SEGMENT_INFO = {
    'running': {
        'icon': u'\u2022',
        'colors': [Color.ROS_RUNNING_FG, Color.ROS_BG]
    },
    'stop': {
        'icon': u'\u2022',
        'colors': [Color.ROS_STOP_FG, Color.ROS_BG]
    }
}


class ROSSegment(Segment):

    @staticmethod
    def ros_get_version():
        # url: http://linux.die.net/man/1/rosversion
        bashCommand = "rosversion -d"
        ros_version = "<unknown>"
        try:
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            ros_version = process.communicate()[0].rstrip()
        except Exception as e:
            print("except: {}" % e)
        finally:
            return ros_version

    @staticmethod
    def ros_rosmaster_enable():
        result = False
        # url: http://stackoverflow.com/a/13333130
        try:
            cmd = "ps -A|grep rosmaster|wc -l"
            ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # url: http://stackoverflow.com/questions/275018/how-can-i-remove-chomp-a-newline-in-python
            output = ps.communicate()[0].rstrip("\n")
        except Exception as e:
            print("except: {}" % e)
        finally:
            result = output == "1"
            return result

    @staticmethod
    def build_segments():
        #
        segments = [
            {
                # url: http://www.fontspace.com/unicode/char/1F422-turtle
                'contents': u'\U0001F422 ',  # unicode d'une tortue
                'colors': [Color.ROS_FG, Color.ROS_BG]
            }
        ]

        # Version ROS
        ros_version = ROSSegment.ros_get_version()
        if ros_version != "<unknown>":
            segments.append({
                'contents': u' {} '.format(ros_version),
                'colors': SEGMENT_INFO['running']['colors']
            })

        # Rosmaster enable ?
        b_rosmaster = ROSSegment.ros_rosmaster_enable()
        if b_rosmaster:
            segments.append({
                'contents': ' %s' % (SEGMENT_INFO['running']['icon']),
                'colors': SEGMENT_INFO['running']['colors']
            })
        else:
            segments.append({
                'contents': ' %s' % (SEGMENT_INFO['stop']['icon']),
                'colors': SEGMENT_INFO['stop']['colors']
            })

        return segments

    @staticmethod
    def build_segment_ros_version():
        segment = {}
        # Version ROS
        ros_version = ROSSegment.ros_get_version()
        if ros_version != "<unknown>":
            segment = {
                'contents': ' %s' % ros_version,
                'colors': SEGMENT_INFO['running']['colors']
            }
        return segment

    def __call__(self, pl, ignore_statuses=[]):
        return self.build_segments()


ros = with_docstring(ROSSegment(),
                     '''ROS
''')


def add_ros_segment(powerline):
    list_dict_segments = ros(None)
    for dict_segment in list_dict_segments:
        color_fg, color_bg = dict_segment['colors']
        powerline.append(dict_segment['contents'], color_fg, color_bg)
