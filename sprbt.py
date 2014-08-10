#!/usr/bin/env python
#
#       Humanitybot: A Cards-Against Humanity IRC Bot
# -----------------------------------------------------------
#      [ https://github.com/Breakthrough/humanitybot ]
#
# Copyright (C) 2014 Brandon Castellano <www.bcastell.com>
# Copyright (c) 2013-2014, Matthew Ames <www.supermatt.net>
#
# Humanitybot is licensed under the BSD 2-Clause License; see the
# included LICENSE file or visit the following page for details:
# https://github.com/Breakthrough/humanitybot
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#

import socket
import ssl
import sys
import re
import threading
import time
from datetime import datetime
from datetime import timedelta
import select
import functions

class IRCConnector(threading.Thread):
    def __init__ (self, server):
        # TODO: Just replace the below with the server dict() directly.
        self.host = server['host']
        self.port = server['port']
        self.channel = server['channel']
        self.use_ssl = server['use_ssl']
        self.hb_interval = server['heartbeat_interval']
        self.hb_last    = time.time()
        self.delay_time = 0.1  # Time to wait in seconds between loop iterations if hb_interval > 0
        self.admin_list = server['admin_list']
        self.botname = server['nickname']   # IRC nickname
        self.ns_pass = server['nickserv_password']
        self.identity = "superbot"
        self.realname = "superbot"
        self.hostname = "supermatt.net"
        self.allmessages = []
        self.lastmessage = datetime.now()
        self.pulsetime = 500
        threading.Thread.__init__ ( self )

    def output(self, message):
        print("Server: %s\nMessage:%s\n" %(self.host, message))

    def say(self, message):
        #print "sending %s" % message
        messagetosend = "PRIVMSG %s :%s\n" %(message["channel"], message["message"])
        self.s.send(messagetosend)

    def run (self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.use_ssl:
                self.s = ssl.wrap_socket(self.s)
        except:
            print 'Failed to create socket'
            sys.exit()

        #remote_ip = socket.gethostbyname(self.host)
        #self.output(remote_ip)

        #self.s.connect((remote_ip, self.port))
        self.s.connect((self.host, self.port))

        # As per issue #3, need to leave socket asynchronous for sending hearbeats.
        if not self.hb_interval > 0:
            self.s.setblocking(1)  # If no heartbeat, set synchronous.
        
        message1 = "NICK %s\r\n" %self.botname
        message2 = 'USER %s %s %s :%s\r\n' % (
            self.identity, self.hostname, self.host, self.realname )
        self.s.send(message1)
        self.s.send(message2)

        g = functions.Game(self)

        while 1:

            #
            # If we need to send a heartbeat/PING... (see issue #3)
            #
            if self.hb_interval > 0:
                # TODO: Only delay if no data/message recieved, then update HB timer.
                time.sleep(self.delay_time)
                if (time.time() - self.hb_last) > self.hb_interval:
                    self.hb_last = time.time()
                    self.s.send("PING %s\n" % self.host)

            line = None
            message = None

            ready = select.select([self.s], [], [], 0.1)
            if ready[0]:
                line = self.s.recv(250)
                print line

            if line:
                #self.output(line)
                line.strip()
                splitline = line.split() #" :")

                if "PING" in splitline[0]:
                    pong = "PONG %s" % splitline[1]
                    self.output(pong)
                    self.s.send(pong)

                ##
                ## [Issue #4] Auto-send NickServ password when MOTD ends
                ## https://github.com/Breakthrough/humanitybot/issues/4
                ##
                ## Replaced with !ns trigger/command until issue resolved.
                ##
                #if re.search(":End of /MOTD command.", line):
                #        joinchannel = "JOIN %s\n" %self.channel
                #        self.output(joinchannel)
                #        self.s.send("PRIVMSG nickserv :identify hum4n1ty\n")
                #        self.s.send(joinchannel)
                #        self.inchannel = True

                if re.search("^:.* NICK .*$", line):
                    nicksplit = line.split()
                    oldnickstring = nicksplit[0][1:]
                    oldnicklist = oldnickstring.split("!")
                    oldnick = oldnicklist[0]
                    newnick = nicksplit[2][1:]
                    for player in g.players:
                        if player.username == oldnick:
                            player.username = newnick

                if re.search("^:.* QUIT .*$", line) or re.search("^:.* PART .*$", line):
                    split1 = line.split()
                    split2 = split1[0].split("!")
                    username = split2[0][1:]
                    print username
                    message = g.part(username)
                    if message:
                        self.allmessages.append({"message": message, "channel": self.channel})

                if re.search("PRIVMSG", line):
                    details = line.split()
                    user = details[0].split("!")
                    username = user[0][1:]
                    channel = details[2]
                    messagelist = details[3:]
                    message = " ".join(messagelist)[1:]
                    lower = message.lower()

                    if channel == self.botname:
                        channel = username

                    if username in self.admin_list:

                        if lower == "!kill":
                            print 'QUIT: %s' % username
                            self.s.send("QUIT :Bot quit\n")

                        elif lower == '!ns': 
                            self.s.send("PRIVMSG nickserv :identify %s\n" % self.ns_pass)

                        elif lower == '!join': 
                            joinchannel = "JOIN %s\n" % self.channel
                            self.output(joinchannel)
                            #self.s.send("PRIVMSG nickserv :identify hum4n1ty\n")
                            self.s.send(joinchannel)
                            self.inchannel = True

#                        elif lower == '$whois': 
#                            joinchannel = "WHOIS supermatt\n"
#                            self.output(joinchannel)
#                            #self.s.send("PRIVMSG nickserv :identify hum4n1ty\n")
#                            self.s.send(joinchannel)
#                            self.inchannel = True

                        elif lower == "!test":
                            self.allmessages.append({"message": "test message", "channel": channel})
                        
                        elif lower == "!reload":
                            try:
                                reload(functions)
                                self.allmessages.append({"message": "Reloaded functions", "channel": channel})
                            except:
                                self.allmessages.append({"message": "Unable to reload due to errors", "channel": channel})
                        else:
                            self.allmessages += functions.actioner(g, message, username, channel, self.channel)

                if re.search(":Closing Link:", line):
                    sys.exit()

            if g.inprogress or g.starttime:
                self.allmessages += functions.gameLogic(g, message, username, channel, self.channel)
            line = None
            message = None
            timestamp = datetime.now()
            if len(self.allmessages) > 0:
                newtime = self.lastmessage + timedelta(milliseconds = self.pulsetime)
                if timestamp > newtime:
                    #print self.allmessages
                    currmess = self.allmessages.pop(0)
                    self.say(currmess)
                    self.lastmessage = timestamp
            #print self.allmessages

# TODO: Move below into separate config/settings file (issue #2).
irc_connections = [{
    "host": "irc.darkmyst.org",
    "port": 6667,
    "nickname": "humanitybot",
    "nickserv_password": "NICKSERV_PASSWORD",
    "channel": "#cah",
    "use_ssl": True,
    "admin_list": [ 'some_admin_nick', 'another_bot_op' ],
    "heartbeat_interval": 120,  # Time in seconds between heartbeat messages (set 0 to disable)
}]

for server in irc_connections:
    IRCThread = IRCConnector(server)
    IRCThread.start()

# Currently does not quit gracefully (issue #5), need to track thread status and !kill messages.

# TODO: Monitor threads (keep a list of refs/connections), restart if required
#       (e.g. thread closes without seeing !kill).
# TODO: Watch for !kill command from any thread - need a message queue
#       (e.g. graceful exit).
