set number
set ignorecase
"use system clipboard
set clipboard=unnamedplus
"space for enter tab
set tabstop=4
"indent when shift line
set shiftwidth=4
" restore cursor position
set mouse=a
if has("autocmd")
  au BufReadPost * if line("'\"") > 0 && line("'\"") <= line("$") | exe "normal! g`\"" | endif
endif

"nmap <Space> <Plug>(easymotion-w)
"nmap <S-Space> <Plug>(easymotion-w)
"vmap <Space> <Plug>(easymotion-w)
"vmap <S-Space> <Plug>(easymotion-w)
"nmap <C-l> <Plug>(easymotion-overwin-line)
"autocmd WinLeave * silent

"autocmd Filetype ipynb nmap <C-s> $a  <Esc>
"autocmd Filetype ipynb vmap <C-p> :!python<CR>
"nmap <C-q> :q<CR>
noremap <M-LeftMouse> <4-LeftMouse>
inoremap <M-LeftMouse> <4-LeftMouse>
onoremap <M-LeftMouse> <C-C><4-LeftMouse>
noremap <M-LeftDrag> <LeftDrag>
inoremap <M-LeftDrag> <LeftDrag>
onoremap <M-LeftDrag> <C-C><LeftDrag>
