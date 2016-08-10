# vim:fileencoding=utf-8:noet
import ast
import requests
from time import time


def datas_up_to_date(httpserver_last_update_time):
    max_delta_time = 2.0    # in ms
    b_datas_up_to_date = False
    try:
        # maj du dernier temps d'update par le serveur HTTP
        cur_time = time()   # in ms
        delta_update_time = cur_time - httpserver_last_update_time
        # print("%s %s %s" % (cur_time, httpserver_last_update_time, delta_update_time))
        b_datas_up_to_date = delta_update_time < max_delta_time
    except Exception, e:
        print("Exception: ", e)
        b_datas_up_to_date = False
    return b_datas_up_to_date


def add_docker_with_daemon_segment(powerline):
    # list_dict_segments = docker(None)

    # for dict_segment in list_dict_segments:
    #     color_fg, color_bg = dict_segment['colors']
    #     powerline.append(dict_segment['contents'], color_fg, color_bg)
    #     # powerline.append_right(dict_segment['contents'], color_fg, color_bg, separator=powerline.separator_right)

    dict_json = {}
    b_reach_httpserver = False
    b_datas_up_to_date = False

    try:
        r = requests.get('http://127.0.0.1:8080/api/v1/getrecord/docker')
        # url: http://stackoverflow.com/questions/988228/converting-a-string-to-dictionary
        dict_json = ast.literal_eval(r.content)
        # print(dict_json)
        b_reach_httpserver = True
        b_datas_up_to_date = datas_up_to_date(dict_json['time'])
    except:
        # except Exception, e:
        # print("Exception: ", e)
        dict_json = {}
        b_reach_httpserver = False

    # print("- dict_json: {}\n\
    #     - b_datas_up_to_date: {}\n\
    #     b_reach_httpserver: {}\n".format(dict_json,
    #                                      b_datas_up_to_date, b_reach_httpserver))
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
