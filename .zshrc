#alias x='startx'
alias s='sudo'
alias ss='sudo systemctl'
alias sp='sudo pacman'
alias sps='sudo pacman -S'
alias spsyu='sudo pacman -Syu'
alias sprs='sp -Rs'
alias psyu='pikaur -Syu'
alias pq='pacman -Qs'
alias p='pikaur'
alias py='python'
alias r='ranger'
alias gg='git grep'
#alias xr='nvidia-xrun qtile'
alias pl='pdflatex tmp.tex tmp.pdf && evince tmp.pdf'
alias pbl='pdflatex tmp.tex && bibtex tmp && pdflatex tmp.tex && pdflatex tmp.tex && evince tmp.pdf'
alias bbl='pdflatex tmp.tex && biber tmp && pdflatex tmp.tex && pdflatex tmp.tex && evince tmp.pdf'
alias ns='nvidia-smi'
alias pipu="pip install --user"

# autoload prompt themes
autoload -Uz promptinit
promptinit
prompt adam2
