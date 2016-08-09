# vim:fileencoding=utf-8:noet
from powerline.segments import Segment, with_docstring
import subprocess
import shelve
from os.path import expanduser
from time import time
import os.path

ROS_STATUSES = ('running')

SEGMENT_INFO = {
    'ros_master_reachable': {
        # 'icon': u'\ua537',
        # 'icon': u'\uf192 ',
        'icon': u'\uf05d ',  # url: rond + check (validation)
        'colors': [Color.ROS_RUNNING_FG, Color.ROS_BG]
    },
    'ros_master_unreachable': {
        # 'icon': u'\ua537',
        # 'icon': u'\uf192 ',
        'icon': u'\uf05c ',  # url: rond + croix (refus)
        'colors': [Color.ROS_STOP_FG, Color.ROS_BG]
    },
    'ros_version': {
        'colors': [Color.ROS_FG, Color.ROS_BG]
    },
    'ros_master_uri': {
        # 'icon': U'\U0001F5A7',  # url: http://www.fileformat.info/info/unicode/char/1f5a7/index.htm
        'icon': u'\uF108',
        'colors': [Color.ROS_MASTER_URI_FG, Color.ROS_MASTER_URI_BG]
    }

}


class ROSSegment(Segment):

    def __init__(self):
        # url: http://stackoverflow.com/questions/4028904/how-to-get-the-home-directory-in-python
        self.home_path = expanduser("~")
        self.db = shelve.open(self.home_path + "/.powerline-shell.ros")

    # url: http://stackoverflow.com/questions/865115/how-do-i-correctly-clean-up-a-python-object
    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

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
    def execute_cmd(cmd, default=""):
        output = ""
        # url: http://stackoverflow.com/a/13333130
        try:
            bashprocess = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # url: http://stackoverflow.com/questions/275018/how-can-i-remove-chomp-a-newline-in-python
            output = bashprocess.communicate()[0].rstrip("\n")
        except Exception as e:
            print("except: {}" % e)
        finally:
            return output

    @staticmethod
    def ros_master_running():
        return ROSSegment.execute_cmd("ps -A|grep rosmaster|wc -l", "0") == "1"

    @staticmethod
    def ros_rostopic_list():
        output = ROSSegment.execute_cmd("rostopic list", "")
        list_topics = output.split('\n')
        return list_topics

    def get_value_from_db(self, key, default=None):
        try:
            value = self.db[key]
        except KeyError:
            value = default
        finally:
            return value

    def set_value_for_db(self, key, value):
        self.db[key] = value

    def ros_master_reachable_with_db(self):
        cur_time = time()
        last_time = self.get_value_from_db('ros_master_reachable.time', 0.0)
        delta_time = cur_time - last_time
        max_delta_time_for_update = 5.0
        # print("delta time: ", delta_time)
        if delta_time > max_delta_time_for_update:
            # print("update db value")
            output = self.execute_cmd("rostopic list; echo $?", "1")
            return_error = output.split('\n')[-1]
            is_reachable = return_error == '0'
            #
            self.set_value_for_db("ros_master_reachable.time", cur_time)
        else:
            # print("used db value")
            is_reachable = self.get_value_from_db('ros_master_reachable.reachable', False)

        # update db
        self.set_value_for_db("ros_master_reachable.reachable", is_reachable)

        return is_reachable

    def ros_master_reachable_with_daemon(self):
        is_reachable = os.path.isfile(self.home_path + "/.powerline-shell.ROS.reachable")
        return is_reachable

    @staticmethod
    def ros_master_uri():
        return ROSSegment.execute_cmd("echo $ROS_MASTER_URI", "")

    @staticmethod
    def ros_env_active():
        return ROSSegment.execute_cmd("which roscore", "") != ""

    def build_segments(self):
        segments = []
        #
        segments.append(ROSSegment.build_segment_ros_logo())

        # Rosmaster reachable ?
        segments.append(self.build_segment_ros_master_reachable())

        # set env ros ?
        if ROSSegment.ros_env_active():
            # ROS version
            segments.append(ROSSegment.build_segment_ros_version())

            # Ros Master URI
            segments.append(ROSSegment.build_segment_ros_master_uri())

        return segments

    @staticmethod
    def build_segment_ros_logo():
        return {
            # url: http://www.fontspace.com/unicode/char/1F422-turtle
            'contents': u'\U0001F422 ',  # unicode d'une tortue
            'colors': [Color.ROS_FG, Color.ROS_BG]
        }

    def build_segment_ros_master_reachable(self):
        #
        # b_rosmaster = self.ros_master_reachable_with_db()
        b_rosmaster = self.ros_master_reachable_with_daemon()
        #
        rosmaster = 'ros_master_reachable' if b_rosmaster else 'ros_master_unreachable'
        segment = {
            'contents': ' %s' % (SEGMENT_INFO[rosmaster]['icon']),
            'colors': SEGMENT_INFO[rosmaster]['colors']
        }
        return segment

    @staticmethod
    def build_segment_ros_master_uri():
        segment = {}
        ros_master_uri = ROSSegment.ros_master_uri().replace('http://', '')
        # ros_master_uri = re.sub(r'[^0-9]', "", ros_master_uri)
        segment = {
            'contents': ' %s  %s' % (SEGMENT_INFO['ros_master_uri']['icon'], ros_master_uri),
            'colors': SEGMENT_INFO['ros_master_uri']['colors']
        }
        return segment

    @staticmethod
    def build_segment_ros_version():
        segment = {}
        # Version ROS
        ros_version = ROSSegment.ros_get_version()
        if ros_version != "<unknown>":
            segment = {
                'contents': ' %s' % ros_version,
                'colors': SEGMENT_INFO['ros_version']['colors']
            }
        return segment

    def __call__(self, pl, ignore_statuses=[]):
        return self.build_segments()


ros = with_docstring(ROSSegment(),
                     '''ROS
''')


def add_ros_segment(powerline):
    pass
