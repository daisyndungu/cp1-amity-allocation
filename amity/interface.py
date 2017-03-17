#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    Amity create_room create_room <room_type> <room_names>...
    Amity add_person <first_name> <last_name> <position> [--a='n']
    Amity delete_event <eventid>
    Amity edit_event <room_name>
    Amity print_room <room_name>
    Amity ticket_invalidation <ticket_id>
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    wants_accomodation --a=<n> [defult: n]
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from amity import Amity

from pyfiglet import Figlet, figlet_format
from termcolor import colored, cprint


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print(colored("Invalid Command!", "red"))
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

border = colored("*" * 20, 'red').center(80)


def introduction():
    print(border)
    cprint(figlet_format('AMITY', font='colossal'),
           'blue', attrs=['bold'])

    print(__doc__)
    print(border)


class Amity(cmd.Cmd):
    amity = Amity()
    prompt = '(Amity)<><> '

    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create_room <room_type> <room_names> ... """
        room_type = args['<room_type>']
        for room_name in args['<room_names>']:
            self.amity.create_room(room_type, room_name)

    @docopt_cmd
    def do_add_person(self, args):
        """Usage: add_person <first_name> <last_name> <position> [--a=n] """
        position = args['<position>']
        person_name = args['<first_name>'] + ' ' + args['<last_name>']
        print(person_name)
        if args['--a'] is None:
            args['--a'] == 'n'
        else:
            want_accomodation = args['--a']
        want_accomodation = args['--a']
        print(want_accomodation)
        self.amity.add_person(position, person_name, want_accomodation)

    @docopt_cmd
    def do_load_people():
        """Usage: load_people """
        self.amity.load_people()

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name> """
        room_name = arg['<room_name>']
        self.amity.print_room(room_name)

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""
        cprint('\t\t\tExitting Amity...Bye', 'magenta')
        option = input("Do you want to save any updates in Amity? (y/n): ")
        if option is 'y' or 'Y':
            print("\t\t\tSaving...")
            self.amity.save_state()
            cprint('\t\t\tSaved...Bye', 'magenta')
        else:
            cprint('\t\t\t...Bye', 'magenta')
        exit()

if __name__ == '__main__':
    introduction()
    try:
        Amity().cmdloop()
    except KeyboardInterrupt:
        cprint('\t\t\tExitting Amity...Bye', 'magenta')
        exit()
