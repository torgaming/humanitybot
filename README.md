
humanitybot
===========

humanitybot is a Python-based IRC bot for playing Cards Against Humanity.  humanitybot includes the official Cards Against Humanity deck, and one can easily add/remove additional cards.

This repository is an actively developed fork of the [original humanitybot](https://github.com/SuperMatt/humanitybot).  Feel free to submit bug reports or feature request to the [humanitybot issue tracker](https://github.com/Breakthrough/humanitybot/issues).


Features
-------------

 - SSL support, multiple server connections
 - nick-based admin commands
 - official Cards Against Humanity deck, easily configurable (see `cards.py`)


Download & Requirements
---------------------------

The latest stable version of humanitybot is `v0.2.0` and can be [downloaded here](https://github.com/Breakthrough/humanitybot/archive/v0.2.0.zip); for other versions, see the [releases page](https://github.com/Breakthrough/humanitybot/releases).

humanitybot depends only on Python 2 (tested on 2.7.3).


Configuration & Running
---------------------------

Once downloaded, you can invoke humanitybot directly via `./sprbt.py`, or through Python itself:

    python sprbt.py

The output from the server is displayed wherever humanitybot is run.  Once connected to a server, humanitybot will sit idle until it recieves the `$join` command from an admin (someone whose nickname is in that server's `admin_list`).  To leave the channel/server, one can use the `$kill` command (the bot will disconnect **immediately**, even during a game).  For a full list of commands, see the list below.


Admin Command List
---------------------------

The following commands can only be used if the nickname of the person appears in the `admin_list` for that particular server:

 - `$join` - makes humanitybot join the configured channel for the server, ready for a game
 - `$kill` - forces humanitybot to disconnect and quit
 - `$test` - test command, should see response from humanitybot
 - `$reload` - reloads all game-logic functions


To-Do List
-------------

 - add official UK & Canadian decks
 - move bot configuration into separate JSON/INI file
 - include changelog / update version information


License
-------------

humanitybot is licensed under BSD-2 Clause; see the LICENSE file for details.

The included cards file (`cards.py`) contains material from the official Cards Against Humanity, distributed under a Creative Commons BY-NC-SA 2.0 license.  See the `cards.py` file for details.
