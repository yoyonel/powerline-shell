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
