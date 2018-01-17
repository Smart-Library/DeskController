#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    smart-library desk --action <action> --name "<name>" --i2c_address <i2c_address>
    smart-library (-i | --interactive)
    smart-library (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys, cmd, re
from docopt import docopt, DocoptExit
from services.desk_handler_service import DeskHandlerService
from colorama import Fore, Style

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, self.format_args(arg))
        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print(Fore.RED + 'Whoops! Something went wrong. Please try again.')
            print(str(e) + Style.RESET_ALL)
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

class MyInteractive (cmd.Cmd):
    intro = 'Welcome to the Smart Library command line interface! (type help for a list of commands.)'
    prompt = '(smart-library) '

    @docopt_cmd
    def do_desk(self, arg):
        """
        Usage: desk --action <action> --name "<name>" --i2c_address <i2c_address>
        
        Options:
        --action Action on a desk [create]
        --name Name of desk to execute action on
        --i2c_address Address on the I2C bus
        """

        action = arg['--action']
        name = arg['--name']
        i2c_address = arg['--i2c_address']

        if action == 'create': 
            status, response = DeskHandlerService.create(name = name, i2c_address = i2c_address)
            if status == DeskHandlerService.SUCCESS_STATUS:
                print(Fore.GREEN + DeskHandlerService.SUCCESSFUL_CREATE + Style.RESET_ALL)
            else:
                print(Fore.RED + DeskHandlerService.FAILED_CREATE)
                print(response + Style.RESET_ALL)
        else: raise DocoptExit('Action on desk is not allowed')

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print(Fore.GREEN + 'See ya!' + Style.RESET_ALL)
        exit()

    def format_args(self, args):
        new_args = []
        
        for index, item in enumerate(args.split()):
            item = re.sub(r'"', '', item)
            if index == 0 or item.startswith("--") or new_args[-1].startswith("--"):
                new_args.append(item)
            else:
                new_args[-1] += f' {item}'

        return new_args

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)
