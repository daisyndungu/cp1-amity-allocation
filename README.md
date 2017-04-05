# cp1-amity-allocation
A command-line application of a room allocation system for one of Andela’s facilities called Amity. This application allows one to create a list of rooms, add person, load the data stored in the application to a database among other functions.

The building blocks are:
  * Python 3
  * Sqlite3
  * Docopt

## Setting It up
These are instructions for setting up Amity Commandline app in development environment.

* prepare directory for project code and virtualenv:

      $ mkdir -p ~/CLIapp

      $ cd ~/CLIapp
* prepare virtual environment (with virtualenv you get pip, we'll use it soon to install requirements):

      $ virtualenv --python=python3 amity-venv

      $ source amity-venv/bin/activate
* check out project code:

      $ git clone https://github.com/daisyndungu/cp1-amity-allocation.git

* install requirements into virtualenv:

      $ pip install -r cp1-amity-allocation/requirements.txt
      
 * Run the application:
 
       $ python amity/interface.py -i
