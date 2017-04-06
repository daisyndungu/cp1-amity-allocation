# cp1-amity-allocation
A command-line application of a room allocation system for one of Andela’s facilities called Amity. This application allows one to create a list of rooms, add person, load the data stored in the application to a database among other functions.

The building blocks are:
  * Python 3
  * Sqlite3
  * Docopt

## INSTALLATION
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
      $ git checkout refactor-OOP
 * Run the application:

       $ python app.py -i
       
 ### COMMANDS AVAILABLE
 * create_room <room_type><room_name(s)>
 
 Creates room(s) where room_type can be either L for livingspace or O for office space. The use can enter one or more room       names
 
       $ (amity)create_room O Hogwarts Camelot
       $ An Office: HOGWARTS has been created...>>
       $ An Office: CAMELOT has been created...>>
       $ (amity)create_room L TOPAZ SCALA
       $ An Office: TOPAZ has been created...>>
       $ An Office: SCALA has been created...>>
 * (Amity)<><>add_person <first_name> <last_name> <position> [want_accomodation]
  
  Adds a person to the system and allocates the person to a random room. Accomodation is optional for fellows but staf can get   allocated to a livingspace. Both fellow and staff get office allocations.
       
       $ (amity)add_person Daisy Ndungu fellow --a=y
       $ Fellow: DAISY NDUNGU has been added...>>
       
 * print_allocations [--o=filename]
 
 This can print to a file or on the screen. For file output use the command :
       
       $ (Amity)<><> print_allocations --o=allocations
     
 this will print to a allocations.txt file.
 
 * reallocate_person <first_name> <last_name> <new_room_name>
 
 ###### Constraints:

        can only move allocate person to room of same type i.e office to office and living space to living space
        the new room should have atleast one vacant space
        staff cannot be relocated to living spaces
  
Also, if the person was not allocated previously, ther will be allocated to the new room and deleted from the list of unallocated people if they missed a room of the same type as the new room.
       
       $ (Amity)<><> reallocate_person DAISY NDUNGU camelot
       $ DAISY NDUNGU has been reallocated successfully...
      
This are some of the command available in amity allocation. Below is a link to a Demo video for all the commands available.

https://asciinema.org/a/2fh67thtlshs5fxo75ugvh30c

