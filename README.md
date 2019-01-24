I(torgaming) did not write this bot but I will try to build on documentation and other stuff to improve from the original software. I also might look into(no promises) changes that https://github.com/Crysknife007/humanitybot did which was also forked from https://github.com/Breakthrough/humanitybot

humanitybot
===========

humanitybot is a Python-based IRC bot for playing Cards Against Humanity.  humanitybot includes the official Cards Against Humanity deck, and one can easily add/remove additional cards.

This repository is an actively developed fork of the [original humanitybot](https://github.com/SuperMatt/humanitybot).  Feel free to submit bug reports or feature request to the [humanitybot issue tracker](https://github.com/Breakthrough/humanitybot/issues).


Features
-------------

 - SSL support, NickServ identification, multiple server connections
 - official Cards Against Humanity deck, easily configurable (see `cards.py`)
 - nick-based administration, see command list below


Download & Requirements
---------------------------

The latest stable version of humanitybot is `v0.3.0` and can be [downloaded here](https://github.com/Breakthrough/humanitybot/archive/v0.3.0.zip); for other versions, see the [releases page](https://github.com/Breakthrough/humanitybot/releases).

humanitybot depends only on Python 2 (tested on 2.7.3).


Configuration & Running
---------------------------

**Configuration**: Once extracted, edit the file `humanitybot_config.py` to setup humanitybot's IRC connection settings ([click here](https://github.com/Breakthrough/humanitybot/blob/master/humanitybot_config.md) to view an example).

**Running**: You can invoke humanitybot directly via `./sprbt.py`, or through Python itself:

    python sprbt.py

The output from the server is displayed wherever humanitybot is run.  Once connected to a server, humanitybot will sit idle until it recieves commands.  Commands are sent to humanitybot by private message, and are only allowed by nicknames in the `admin_list` for that server (as defined in the bot configuration).

You can send humanitybot the `!ns` command to identify itself to NickServ (you should pre-register a nickname for the bot, and enter the appropriate nickname/password in the config file).  Once identified (or if the server doesn't use NickServ), sending the `!join` command will make humanitybot join the channel defined for that server.  For a full list of admin commands, see the list below.

At this point, players can enter the game and start playing.  People can join the game by typing `join` in the channel, and can leave/exit the game by typing `part`.


Admin Command List
---------------------------

The following commands can only be used if the nickname of the person appears in the `admin_list` for that particular server:

 - `!ns` - tells humanitybot to identify itself to NickServ (sends password defined in the config file)
 - `!join` - makes humanitybot join the configured channel for the server, ready for a game
 - `!kill` - **humanitybot must be manually killed after this command ([issue #5](https://github.com/Breakthrough/humanitybot/issues/5), but *does* at least gracefully disconnect from the server)** - forces humanitybot to disconnect and quit
 - `!test` - test command, should see response from humanitybot
 - `!reload` - reloads all game-logic functions


To-Do List
-------------

 - add official UK & Canadian decks
 - move bot configuration into separate JSON/INI file
 - update version information
 - handle graceful termination/quitting


License
-------------

humanitybot is licensed under BSD-2 Clause; see the LICENSE file for details.

The included cards file (`cards.py`) contains material from the official Cards Against Humanity, distributed under a Creative Commons BY-NC-SA 2.0 license.  See the `cards.py` file for details.
