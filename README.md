# Quick and Dirty Mac Development Environment Setup

Run `python3 set_up_environment.py` to just install all the things.

Run `python3 set_up_environment.py --help` to see install options, such as:

```zsh
# Configure your git user and install all the things.
python3 set_up_environment.py --git-name '<your-name>' --git-email <your-email> 

# All the things, plus install your desired Python version as the default interpreter.
python3 set_up_environment.py --python-version 3.12.1
```


# TODOs

* Add a `rg` and `sed` search and replace alias
rg overhead_press --files-with-matches | xargs sed -i '' 's/overhead_press/arnold_press/g'
