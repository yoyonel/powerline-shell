# vim:fileencoding=utf-8:noet


def add_ros_full_segment(powerline):
    logger = powerline.logger

    logger.debug("[ros_full] add_ros_full_segment: bash_pid=%s" % powerline.bash_pid)

    # on transmet le pid du bash et un logger au ROS segment (builder)
    list_dict_segments = ros(logger, powerline.bash_pid)

    for dict_segment in list_dict_segments:
        try:
            color_fg, color_bg = dict_segment['colors']
            powerline.append(dict_segment['contents'], color_fg, color_bg)
        except Exception, e:
            pass
