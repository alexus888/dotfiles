from os.path import join, expanduser, exists
from subprocess import run
from os import symlink


HOME_DIR = expanduser("~")
DOTS_DIR = join(HOME_DIR, "dotfiles")
LAZY_DIR = join(HOME_DIR, ".config", "nvim")
PYTHON_VERSION = "3.12.1"


def main():
    install()


def install():
    commands = (
        # general
        f"mv ~/.zshrc ~/.zshrc.bak",
        f"cat {join(DOTS_DIR, ".zshrc")} > {join(HOME_DIR, ".zshrc")},
        "brew update",
        "brew install nvim tree ripgrep",

        # python
        "brew install pyenv pipx",
        f"pyenv install {PYTHON_VERSION}",
        f"pyenv global {PYTHON_VERSION}",
        "pipx install poetry",
        "pipx install pipenv",
        "pipx ensurepath",

        # javascript
        "brew install node",

        # git
        "npm install -g git-split-diffs",
        ("git", "config", "--global", "core.pager", "git-split-diffs --color | less -RFX", ),

        # editor
        f"rm -rf {LAZY_DIR}",
        f'git clone https://github.com/lazyvim/lazyvim.git {LAZY_DIR}',
    )

    for command in commands:
        if isinstance(command, str):
            print(command)
            run(command.split(" "), check=True)
        else:
            print(" ".join(command))
            run(command, check=True)


if __name__ == "__main__":
    main()
