#!/usr/bin/env bash
cd "$(dirname $0)/python"
CHOOSE(){
    clear
    printf "Welcome to Python Words!\n\nWhat would you like to do?\n\n\n1. Create Puzzles\n2. Play Puzzles\n3. Exit\n\n"
    read -r SELECTION
    printf "\n\n"
    case $SELECTION in
        1) python3 puzzle_creator.py; CHOOSE;;
        2) python3 wordfinder.py; CHOOSE;;
        3) echo "bye";;
        *) printf "\nInvalid response\n\n"; CHOOSE;;
    esac
}

CHOOSE
