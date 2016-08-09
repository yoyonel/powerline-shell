# vim:fileencoding=utf-8:noet


def add_ros_full_segment(powerline):
    list_dict_segments = ros(None)

    for dict_segment in list_dict_segments:
        color_fg, color_bg = dict_segment['colors']
        powerline.append(dict_segment['contents'], color_fg, color_bg)
