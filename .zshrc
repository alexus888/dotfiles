export PATH="${HOMEBREW_PREFIX}/opt/openssl/bin:$PATH"

# `pyenv`
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# aliases
alias python="python3"
alias atree="tree --gitignore"
