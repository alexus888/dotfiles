from os.path import join, expanduser
import subprocess
import artifacts
from importlib import resources
from datetime import datetime
from typing import List, Union
from argparse import ArgumentParser, Namespace


HOME_DIR = expanduser("~")
LAZY_DIR = join(HOME_DIR, ".config", "nvim")
PYTHON_VERSION = "3.12.1"
POSTGRES_VERSION = "14"


def main():
    cli = ArgumentParser()
    cli.add_argument(
        "--python-version",
        help=f"Install the provided Python version or default to {PYTHON_VERSION}",
        action="store",
        default=PYTHON_VERSION,
    )
    cli.add_argument(
        "--git-name",
        help="Configure the global git user.",
        type=str,
        action="store",
    )
    cli.add_argument(
        "--git-email",
        help="Configure the global git email.",
        type=str,
        action="store",
    )
    arguments = cli.parse_args()
    configs()
    dependencies()
    applications()
    editor()
    python(arguments)
    git(arguments)
    print("Done! Please restart your shell to effect changes.")


def configs():
    now = datetime.now()
    filenames = [".zshrc", ".gitconfig", ".pythonstartup"]
    for filename in filenames:
        bak = join(HOME_DIR, f"{filename}.{now}.bak")
        old = join(HOME_DIR, filename)
        try:
            print(f"Backing up {filename}...")
            with open(old, "r") as old_file:
                with open(bak, "w") as bak_file:
                    bak_file.write(old_file.read())
        except FileNotFoundError:
            print(f"{filename} not found, skipping backup...")

        new = resources.files(artifacts).joinpath(filename)
        with open(old, "w") as old_file:
            old_file.write(new.read_text())


GENERAL = (
    "brew update",
    "brew upgrade",
    "brew install bat graphviz ripgrep tree choose-rust",
)

JAVASCRIPT = (
    "brew install node",
    # TODO: add nvm and handle .zshrc config
)


POSTGRES = (f"brew install postgresql@{POSTGRES_VERSION}",)


def dependencies():
    print("Setting up environment...")

    print("Updating brew and installing general utilities...")
    run_multiple(GENERAL)

    print("Installing JavaScript environment management tools...")
    run_multiple(JAVASCRIPT)

    print("Installing PostgreSQL...")
    run_multiple(POSTGRES)


def applications():
    APPLICATIONS = (
        "brew install iterm2",
        "brew install tableplus",
    )
    print("Installing applications...")
    for command in APPLICATIONS:
        try:
            run(command)
        except subprocess.CalledProcessError as ex:
            print(ex)


def editor():
    print("Installing LazyVim...")
    EDITOR = (
        "brew install neovim",
        f"rm -rf {LAZY_DIR}",
        # NOTE: at some point this may become your own LazyVim config repo.
        f"git clone https://github.com/LazyVim/starter {LAZY_DIR} --depth 1 --single-branch",
    )
    run_multiple(EDITOR)

    # port python LSP and visible dotfiles configuration
    print("Porting existing LazyVim configurations...")
    filename = "lazy.lua"
    old = join(LAZY_DIR, "lua", "config", filename)
    new = resources.files(artifacts).joinpath(filename)
    with open(old, "w") as old_file:
        old_file.write(new.read_text())


def git(arguments: Namespace):
    print("Installing Git configuration...")
    GIT = (
        # pretty GitHub-style split diffs
        "npm install -g git-split-diffs",
        # git completion
        f"curl -o {join(HOME_DIR, 'git-completion.bash')} https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash",
        f"curl -o {join(HOME_DIR, '_git')} https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.zsh",
    )
    for command in GIT:
        run(command)
    if arguments.git_name:
        run(["git", "config", "--global", "user.name", arguments.git_name])
    if arguments.git_email:
        run(["git", "config", "--global", "user.email", arguments.git_email])


def python(arguments: Namespace):
    PYTHON = (
        "brew install pyenv pipx pyenv-virtualenv",
        "pipx install poetry",
        "poetry config virtualenvs.in-project true",
        "pipx install pipenv",
        "pipx ensurepath",
    )
    print("Installing Python environment management tools...")
    for command in PYTHON:
        run(command)

    python_version = arguments.python_version

    if python_version:
        print(
            f"Installing Python {python_version}. Hang tight, this may take a second..."
        )
        run(f"pyenv install {python_version} --skip-existing")
        run(f"pyenv global {arguments.python_version}")
    run("pip install rich")


def run_multiple(commands):
    for command in commands:
        run(command)


def run(command: Union[str, List]):
    if isinstance(command, str):
        print(command)
        subprocess.run(command.split(" "), check=True)
    else:
        print(" ".join(command))
        subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
