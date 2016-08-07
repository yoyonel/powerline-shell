CHROOT=`ls -di / | awk '{if ($1 != "2") print 1; else print 0;}'`
function _update_ps1() {
    if [ "$TERM" != "linux" ] ; then
       if [ "$(uname)" == "Darwin" ]; then
          update_terminal_cwd
       fi
       PREV=$?
       EXTRA=`logname`@`hostname`

       export PS1="$(~/.powerline-shell.py ${PREV} --cwd-max-depth 4)"

       # result_from_python_script=$(~/.powerline-shell.py ${PREV} --width ${COLUMNS} --chroot ${CHROOT} --extra ${EXTRA})
       
       # pws_segment_left="$(~/.powerline-shell.py ${PREV} --cwd-max-depth 4 --width ${COLUMNS} --chroot ${CHROOT} --extra ${EXTRA} --pos_segment left)"
       # pws_segment_right="$(~/.powerline-shell.py ${PREV} --cwd-max-depth 4 --width ${COLUMNS} --chroot ${CHROOT} --extra ${EXTRA} --pos_segment right)"
       # pws_segment_down="$(~/.powerline-shell.py ${PREV} --cwd-max-depth 4 --width ${COLUMNS} --chroot ${CHROOT} --extra ${EXTRA} --pos_segment down)"

       # prompt=$(echo $pws_segment_left '\n' $pws_segment_down)
       # export PS1=$prompt
       # export PS1=""
       # printf '%*b' ${COLUMNS} $pws_segment_right
    fi
}

export PROMPT_COMMAND="_update_ps1"
