# Python Project

## Table of contents:
  - [About]()
  - [Installation and Quick-Start]()
    - [Installation]()
    - [Quick-Start]()
  - [Known bugs]()
  - [To do]()
  - [Collaborators]()


## About
  This project was made for Python Course in MIPT. Using this game, you can play checkers alone, with bot or with your firend on local network.
  There are three available offline modes: Player vs Bot, Player vs Player (Manual mode), Bot vs Bot.
  In multiplayer mode, by now, available opponent selection by setting up his 'ip address'.

  You can manage the game sessions, you've played earlier. For example, you can save the game sessions into file and load them whenever you want.
  With editing config menu, you can customize a bunch of settings (also supports file saves).


## Installation and Quick-Start

  ### Installation

    If you are using MacOSX, install the game, using this command sequence:

    ```
    git clone --branch dev git@github.com:Plovel/PythonProject2.git CheckersGame
    cd CheckersGame
    brew install python3 pip
    pip install requirentments.txt
    ./run.sh
    ```

    If you are using Ubuntu(or other ubuntu-type system), unstall the game, using next command sequence:

    ```
    git clone --branch dev git@github.com:Plovel/PythonProject2.git CheckersGame
    cd CheckersGame
    sudo apt install python3
    pip install requirentments.txt
    ./run.sh
    ```

    If you want to get your ip address for local game, enter this command to the command line:

    ```
    ip address
    ```

  ### Quick-Start

    You can use mouse navigation, but in the menus you can also use 'tab-enter' and arrows to navigate.
    To see all the Hotkeys, available in current menu, press 'X'.
    DON'T PRESS 'T' BUTTON!!!


## Known Bugs

  ### Network issues:

    This part of the game conceptually isn't finished, so it can be inconvenient to use. There are a lot of crash cases were noticed, but it should't affect your game saves and config.


  ### Other issues:

    The rest part of the game should be pretty stable. Serious functional bugs weren't noticed.

## To do
  - \(Most likely) Menu impovements
  - Rework network mechanics

## Collaborators
  [Pavel Sidletskiy](t.me/vendor_vachupa)
