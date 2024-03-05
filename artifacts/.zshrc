export PATH="${HOMEBREW_PREFIX}/opt/openssl/bin:$PATH"

# `psql`
export PSQL_EDITOR="/opt/homebrew/bin/nvim"

# `pyenv`
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
# NOTE: this is virtualenv auto-activate magic, but I don't want that so this is a reminder why.
# eval "$(pyenv virtualenv-init -)"  

# Python REPL
export PYTHONSTARTUP=$HOME/.pythonstartup

# aliases
alias help="cat ~/.zshrc | grep 'alias'"
alias python="python3"
alias hotspots="git log --format=format: --name-only | egrep -v '^$' | egrep '.py' | sort | uniq -c | sort -r"

# alias-prefixed commands
alias atree="tree --gitignore --filesfirst"

# git completion https://www.oliverspryn.com/blog/adding-git-completion-to-zsh
zstyle ':completion:*:*:git:*' script ~/git-completion.bash
fpath=(~/ $fpath)

autoload -Uz compinit && compinit
