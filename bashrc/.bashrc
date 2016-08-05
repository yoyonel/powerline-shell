PS1="[e[1;33m][ u[e[1;37m]@[e[1;32m]h[e[1;33m] W$(git branch 2> /dev/null | grep -e '* ' | sed 's/^..(.*)/ {[e[1;36m]1[e[1;33m]}/') ][e[0m]n==> "
function _update_ps1()
{
export PS1="$(~/powerline-shell.py  --cwd-max-depth 2 $?)"
}
export PROMPT_COMMAND="_update_ps1"

