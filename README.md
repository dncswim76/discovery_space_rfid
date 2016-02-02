# discovery_space_rfid

## Prerequisites

1. Python 2.7
2. pip
3. virtualenv
   `$ pip install virtualenv`
4. virtualenvwrapper
```
   $ pip install virtualenvwrapper
   $ export WORKON_HOME=~/Envs
   $ source /usr/local/bin/virtualenvwrapper.sh
```

## To get started:

1. Clone the repository and cd into directory:
   `$ git clone git@github.com:jdn5126/discovery_space_rfid.git`

2. cd into directory:
   `$ cd discovery_space_rfid`

2. Create a virtual environment:
   `$ mkvirtualenv psucse`

3. Activate virtual environment:
   `$ workon psucse`

4. (Optional) Add the following to ~/.bash_profile:
   `alias psucse="cd ~/discovery_space_rfid; workon psucse"`

5. Install requirements:
   `$ pip install -r requirements/requirements.txt`
