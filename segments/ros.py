# vim:fileencoding=utf-8:noet
from powerline.segments import Segment, with_docstring
import subprocess
import shelve
from os.path import expanduser
from time import time
import os.path
import ast
import requests
import sqlite3

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
    'ros_daemon_not_up_to_date': {
        'icon': u'\u2370 ',  # => Apl functional symbol quad question: ⍰
        'colors': [Color.ROS_DAEMON_NOT_UP_TO_DATE_FG, Color.ROS_BG]
    },
    'ros_topics_number': {
        'icon': u'\u2341',  # => Apl functional symbol quad slash: ⍁
        'colors': [Color.ROS_FG, Color.ROS_BG]
    },
    'ros_nodes_number': {
        'icon': u'\u2b2d',  # => White horizontal ellipse: ⬭
        'colors': [Color.ROS_FG, Color.ROS_BG]
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
        self.httpserver_last_update_time = 0.0
        self.logger = None
        self.bash_pid = 0
        self.dict_json = {}
        self.b_reach_server = False

    # url: http://stackoverflow.com/questions/865115/how-do-i-correctly-clean-up-a-python-object
    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

    def ros_get_version(self):
        # url: http://linux.die.net/man/1/rosversion
        bashCommand = "rosversion -d"
        ros_version = "<unknown>"
        try:
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            ros_version = process.communicate()[0].rstrip()
        except Exception as e:
            # self.logger.debug("except: {}" % e)
            pass
        finally:
            return ros_version

    def execute_cmd(self, cmd, default=""):
        output = ""
        # url: http://stackoverflow.com/a/13333130
        try:
            bashprocess = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # url: http://stackoverflow.com/questions/275018/how-can-i-remove-chomp-a-newline-in-python
            output = bashprocess.communicate()[0].rstrip("\n")
        except Exception as e:
            # self.logger.debug("except: {}" % e)
            pass
        finally:
            return output

    def ros_master_running(self):
        return self.execute_cmd("ps -A|grep rosmaster|wc -l", "0") == "1"

    def ros_rostopic_list(self):
        output = self.execute_cmd("rostopic list")
        list_topics = output.split('\n')
        return list_topics

    def ros_rostopic_number(self):
        # is_reachable = os.path.isfile(self.home_path + "/.powerline-shell.ROS.topics")
        output = self.execute_cmd("sed -e '$!d' ~/.powerline-shell.ROS.topics", 0)
        return output

    def ros_rostopic_number_with_httpserver(self):
        nb_topics = -1
        if self.dict_json:
            nb_topics = 0
            try:
                nb_topics = self.dict_json['topics']
            except KeyError:
                nb_topics = -1
        return nb_topics

    def ros_rosnode_number_with_httpserver(self):
        nb_nodes = -1
        if self.dict_json:
            nb_nodes = 0
            try:
                nb_nodes = self.dict_json['nodes']
            except KeyError:
                nb_nodes = -1
        return nb_nodes

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
        # self.logger.debug("delta time: ", delta_time)
        if delta_time > max_delta_time_for_update:
            # self.logger.debug("update db value")
            output = self.execute_cmd("rostopic list; echo $?", "1")
            return_error = output.split('\n')[-1]
            is_reachable = return_error == '0'
            #
            self.set_value_for_db("ros_master_reachable.time", cur_time)
        else:
            # self.logger.debug("used db value")
            is_reachable = self.get_value_from_db('ros_master_reachable.reachable', False)

        # update db
        self.set_value_for_db("ros_master_reachable.reachable", is_reachable)

        return is_reachable

    def ros_master_reachable_with_daemon_httpserver(self):
        ros_master_reachable = False
        try:
            ros_master_reachable = self.dict_json['reachable'] == '1'
        except KeyError:
            ros_master_reachable = False
        finally:
            return ros_master_reachable

    def ros_master_reachable_with_daemon_files(self):
        is_reachable = os.path.isfile(self.home_path + "/.powerline-shell.ROS.reachable")
        return is_reachable

    def ros_master_uri(self):
        return self.execute_cmd("echo $ROS_MASTER_URI")

    def ros_env_active(self):
        return self.execute_cmd("which roscore") != ""

    @staticmethod
    def build_segment_ros_logo():
        return {
            # url: http://www.fontspace.com/unicode/char/1F422-turtle
            'contents': u'\U0001F422 ',  # unicode d'une tortue
            'colors': [Color.ROS_FG, Color.ROS_BG]
        }

    def build_segment_ros_master_reachable(self):
        #
        segment = {}
        # b_rosmaster = self.ros_master_reachable_with_db()
        if self.b_reach_server:
            b_rosmaster = self.ros_master_reachable_with_daemon_httpserver()
            #
            if self.b_datas_up_to_date:
                rosmaster = 'ros_master_reachable' if b_rosmaster else 'ros_master_unreachable'
            else:
                rosmaster = 'ros_daemon_not_up_to_date'
            segment = {
                'contents': ' %s' % (SEGMENT_INFO[rosmaster]['icon']),
                'colors': SEGMENT_INFO[rosmaster]['colors']
            }
        return segment

    def build_segment_ros_master_uri(self):
        segment = {}
        ros_master_uri = self.ros_master_uri().replace('http://', '')
        # ros_master_uri = re.sub(r'[^0-9]', "", ros_master_uri)
        segment = {
            'contents': ' %s  %s' % (SEGMENT_INFO['ros_master_uri']['icon'], ros_master_uri),
            'colors': SEGMENT_INFO['ros_master_uri']['colors']
        }
        return segment

    def build_segment_ros_version(self):
        segment = {}
        # Version ROS
        ros_version = self.ros_get_version()
        if ros_version != "<unknown>":
            segment = {
                'contents': ' %s' % ros_version,
                'colors': SEGMENT_INFO['ros_version']['colors']
            }
        return segment

    def build_segment_ros_topics(self):
        segment = {}
        if self.b_reach_server:
            #
            ros_topics_number = self.ros_rostopic_number_with_httpserver()
            if ros_topics_number != "0":
                SEGMENT_INFO_colors = 'ros_topics_number' if self.b_datas_up_to_date else 'ros_daemon_not_up_to_date'
                segment = {
                    'contents': ' %s %s' % (SEGMENT_INFO['ros_topics_number']['icon'], ros_topics_number),
                    'colors': SEGMENT_INFO[SEGMENT_INFO_colors]['colors']
                }
        return segment

    def build_segment_ros_nodes(self):
        segment = {}
        if self.b_reach_server:
            #
            ros_nodes_number = self.ros_rosnode_number_with_httpserver()
            if ros_nodes_number != "0":
                SEGMENT_INFO_colors = 'ros_nodes_number' if self.b_datas_up_to_date else 'ros_daemon_not_up_to_date'
                segment = {
                    'contents': ' %s %s' % (SEGMENT_INFO['ros_nodes_number']['icon'], ros_nodes_number),
                    'colors': SEGMENT_INFO[SEGMENT_INFO_colors]['colors']
                }
        return segment

    def datas_up_to_date(self):
        max_delta_time = 2000.0    # in ms
        try:
            httpserver_last_update_time = float(self.dict_json['time'])    # in ms
            # maj du dernier temps d'update par le serveur HTTP
            # self.httpserver_last_update_time = httpserver_cur_update_time
            cur_time = time() * 1000    # in ms
            delta_update_time = cur_time - httpserver_last_update_time
            # self.logger.debug("%s %s %s" % (cur_time, httpserver_last_update_time, delta_update_time))
            self.b_datas_up_to_date = delta_update_time < max_delta_time
        except Exception, e:
            # self.logger.debug("[ros.py] Exception: ", e)
            self.b_datas_up_to_date = False

    def build_segments(self):
        segments = []
        #
        segments.append(ROSSegment.build_segment_ros_logo())

        # Rosmaster reachable ?
        segments.append(self.build_segment_ros_master_reachable())

        # set env ros ?
        if self.ros_env_active():
            # ROS version
            segments.append(self.build_segment_ros_version())

            # Ros Master URI
            segments.append(self.build_segment_ros_master_uri())

            if self.ros_master_reachable_with_daemon_httpserver():
                # Ros Topics number
                segments.append(self.build_segment_ros_topics())

                # Ros Nodes number
                segments.append(self.build_segment_ros_nodes())

        return segments

    @staticmethod
    def select_column_and_value(conn, sql_query, parameters=()):
        """
        urls:
        - http://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
        -> http://stackoverflow.com/a/33108733

        :param conn:
        :param sql_query:
        :param parameters:
        :return:
        """
        execute = conn.execute(sql_query, parameters)
        fetch = execute.fetchone()

        if fetch is None:
            return {}

        return {k[0]: v for k, v in list(zip(execute.description, fetch))}

    def get_dict_json_from_httpserver(self):
        """

        :return:
        """
        dict_json = {}
        b_reach_httpserver = False
        try:
            url = 'http://127.0.0.1:8080/api/v1/getrecord/ros/' + str(self.bash_pid)
            self.logger.debug("[ros.py] url: %s" % url)
            r = requests.get(url)

            # url: http://stackoverflow.com/questions/988228/converting-a-string-to-dictionary
            dict_json = ast.literal_eval(r.content)
            self.logger.debug("HTTP - dict_json: %s" % dict_json)
            b_reach_httpserver = True
        except Exception, e:
            self.logger.debug("Exception: %s" % e)

        return dict_json, b_reach_httpserver

    def get_dict_json_from_db(self):
        """

        :return:
        """
        dict_json = {}
        b_reach_dbserver = False
        try:
            # etablish connection to DB server
            conn = sqlite3.connect('/home/atty/Prog/powerline/powerline-shell_yoyonel/sqlite/pls.db')

            try:
                sql_query = "SELECT * FROM ros WHERE bashid = %s" % self.bash_pid
                dict_json = self.select_column_and_value(conn, sql_query)
                dict_json['reachable'] = str(dict_json['reachable'])
                b_reach_dbserver = True
                #
                self.logger.debug("DB - sql_query: %s" % sql_query)
                self.logger.debug("DB - self.dict_json_from_db: %s" % dict_json)
            except Exception, e:
                self.logger.debug("DB - SELECT - Exception: %s" % e)

            # close connection
            conn.close()
        except Exception, e:
            self.logger.debug("DB - CONNECT - Exception: %s" % e)

        return dict_json, b_reach_dbserver

    def __call__(self, pl, bash_pid, ignore_statuses=[]):
        self.logger = pl
        self.bash_pid = str(bash_pid)

        # recuperation des donnees via le server DB
        # si erreur, on recupere via le serveur HTTP [debug mode]
        dict_json_db, b_reach_server_db = self.get_dict_json_from_db()
        if b_reach_server_db:
            self.dict_json = dict_json_db
            self.b_reach_server = b_reach_server_db
            self.logger.debug("ROS - get datas from DB Server!")
        else:
            self.dict_json, self.b_reach_server = self.get_dict_json_from_httpserver()
            self.logger.debug("ROS - get datas from HTTP Server!")

        self.datas_up_to_date()

        return self.build_segments()


ros = with_docstring(ROSSegment(),
                     '''ROS
''')


def add_ros_segment(powerline):
    pass
