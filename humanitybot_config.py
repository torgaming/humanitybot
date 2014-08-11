#
# HUMANITYBOT CONFIGURATION
#

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
