# vim:fileencoding=utf-8:noet


def add_ros_logo_segment(powerline):
    dict_segment = ROSSegment.build_segment_ros_logo()
    color_fg, color_bg = dict_segment['colors']
    powerline.append(dict_segment['contents'], color_fg, color_bg)
