#!/usr/bin/bash
cd "$(dirname $0)/python"
CHOOSE(){
 printf "Welcome to Python Words!\n\nWhat would you like to do?\n\n\n1. Create Puzzles\n2. Play Puzzles\n3. Exit\n"
 read -r SELECTION
 case $SELECTION in
  1) python3 ~/Coding-Projects/python-words/python/puzzle_creator.py; CHOOSE;;
  2) python3 ~/Coding-Projects/python-words/python/wordfinder.py; CHOOSE;;
  3) echo "bye";;
  *) printf "\nInvalid response\n\n"; CHOOSE;;
 esac
}

CHOOSE
