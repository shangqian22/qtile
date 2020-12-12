alias s='sudo'
alias ss='sudo systemctl'
alias p='pikaur'
alias ps='pikaur -S'
alias psyu='pikaur -Syu'
alias sp='sudo pacman'
alias sps='sudo pacman -S'
alias pq='pacman -Qs'
alias py='python'
alias rg='ranger'
alias vq='vi .config/qtile/config.py'
alias gg='git grep'

# autoload prompt themes
autoload -Uz promptinit
promptinit
#prompt off
prompt adam2
