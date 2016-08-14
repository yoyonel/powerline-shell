# vim:fileencoding=utf-8:noet
import ast
import requests
from time import time
import sqlite3


def datas_up_to_date(httpserver_last_update_time, max_delta_time=2.0):
    b_datas_up_to_date = False
    try:
        # maj du dernier temps d'update par le serveur HTTP
        cur_time = time()   # in ms
        delta_update_time = cur_time - httpserver_last_update_time
        # print("%s %s %s" % (cur_time, httpserver_last_update_time, delta_update_time))
        b_datas_up_to_date = delta_update_time < max_delta_time
    except:
        # except Exception, e:
        # print("Exception: ", e)
        pass
    finally:
        return b_datas_up_to_date


def add_docker_with_daemon_segment_httpserver(powerline):
    dict_json = {}
    b_reach_httpserver = False
    b_datas_up_to_date = False

    try:
        r = requests.get('http://127.0.0.1:8080/api/v1/getrecord/docker')
        # url: http://stackoverflow.com/questions/988228/converting-a-string-to-dictionary
        dict_json = ast.literal_eval(r.content)
        # print(dict_json)
        b_reach_httpserver = True
        httpserver_last_update_time = dict_json['time']
        b_datas_up_to_date = datas_up_to_date(httpserver_last_update_time)
    except:
        # except Exception, e:
        # print("Exception: ", e)
        pass

    # print("- dict_json: {}\n\
    #     - b_datas_up_to_date: {}\n\
    #     - b_reach_httpserver: {}\n".format(dict_json, b_datas_up_to_date, b_reach_httpserver))
    if b_reach_httpserver:
        try:
            list_dict_segments = dict_json["segments"]
            if b_datas_up_to_date:
                for dict_segment in list_dict_segments:
                    color_fg, color_bg = dict_segment['colors']
                    powerline.append(dict_segment['contents'], color_fg, color_bg)
            else:
                for dict_segment in list_dict_segments:
                    _, color_bg = dict_segment['colors']
                    powerline.append(dict_segment['contents'], Color.DOCKER_DAEMON_NOT_UP_TO_DATE_FG, color_bg)
        except KeyError:
            pass


def add_docker_with_daemon_segment(powerline):
    add_docker_with_daemon_segment_httpserver(powerline)
    # add_docker_with_daemon_segment_db_server(powerline)


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


def get_dict_json_from_db(db_filename, logger):
        """

        :return:
        """
        dict_json = {}
        b_reach_dbserver = False

        try:
            # etablish connection to DB server
            conn = sqlite3.connect(db_filename)

            try:
                sql_query = """SELECT * FROM docker WHERE uuid_system = "%s" """ % "uuid"
                dict_json = select_column_and_value(conn, sql_query)
                b_reach_dbserver = True
                #
                logger.debug("DB - docker - sql_query: %s" % sql_query)
                logger.debug("DB - docker - self.dict_json_from_db: %s" % dict_json)
            except Exception, e:
                logger.debug("DB - SELECT - Exception: %s" % e)

            # close connection
            conn.close()
        except Exception, e:
            logger.debug("DB - CONNECT - Exception: %s" % e)

        return dict_json, b_reach_dbserver


def add_docker_with_daemon_segment_db_server(powerline):
    """

    :param powerline:
    :return:
    """
    logger = powerline.logger

    dict_json = {}
    b_reach_dbserver = False
    b_datas_up_to_date = False

    db_filename = '/home/atty/Prog/powerline/powerline-shell_yoyonel/sqlite/pls.db'

    try:
        dict_json, b_reach_dbserver = get_dict_json_from_db(db_filename, logger)
    except Exception, e:
        logger.debug("Exception: {}".format(e))

    try:
        dbserver_last_update_time = dict_json['time']
        b_datas_up_to_date = datas_up_to_date(dbserver_last_update_time)
    except Exception, e:
        logger.debug("Exception: {}".format(e))

    # print("- dict_json: {}\n\
    #     - b_datas_up_to_date: {}\n\
    #     - b_reach_httpserver: {}\n".format(dict_json, b_datas_up_to_date, b_reach_httpserver))
    logger.debug("Docker - add_docker_with_daemon_segment_db_server - b_reach_dbserver: {}".format(b_reach_dbserver))

    if b_reach_dbserver:
        try:
            list_dict_segments = ast.literal_eval(dict_json["segments"])
            logger.debug("Docker - add_docker_with_daemon_segment_db_server - list_dict_segments: {}".format(list_dict_segments))
            logger.debug("Docker - add_docker_with_daemon_segment_db_server - b_datas_up_to_date: {}".format(b_datas_up_to_date))
            if b_datas_up_to_date:
                for dict_segment in list_dict_segments:
                    color_fg, color_bg = dict_segment['colors']
                    logger.debug("Docker - color_fg, color_bg: {} {} {} {}".format(color_fg, color_bg, type(color_fg), type(color_bg)))
                    powerline.append(dict_segment['contents'], color_fg, color_bg)
            else:
                for dict_segment in list_dict_segments:
                    _, color_bg = dict_segment['colors']
                    powerline.append(dict_segment['contents'], Color.DOCKER_DAEMON_NOT_UP_TO_DATE_FG, color_bg)
        except Exception, e:
            logger.debug("Docker - add_docker_with_daemon_segment_db_server - exception: {}".format(e))