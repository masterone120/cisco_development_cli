# import paramiko
#
# from flask import request, render_template
#
# from App import Devices


# router_ip = "192.168.5.11"
# router_username = "alisfactory"
# router_password = "Ad56#33n$xw3"
#
# ssh = paramiko.SSHClient()
#
# # Load SSH host keys.
# ssh.load_system_host_keys()
# # Add SSH host key automatically if needed.
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # Connect to router using username/password authentication.
# ssh.connect(router_ip,
#             username=router_username,
#             password=router_password,
#             look_for_keys=False)
#
# # Run command.
# ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sho running-config")
#
# output = ssh_stdout.readlines()
# # Close connection.
# ssh.close()
#
# # Analyze show ip route output
# for line in output:
#     if "" in line:
#         print(line)
#
# # ------------------------------------------------------------------------------
# # import paramiko
# # import getpass
# # import time
# #
# #
# # HOST = '192.168.5.11'
# # user = 'alisfactory'
# # password = 'Ad56#33n$xw3'
# # ssh = paramiko.SSHClient()
# # ssh_client = paramiko.SSHClient()
# # ssh.load_system_host_keys()
# # ssh = set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # ssh_client.connect(host=HOST, username=user, password=password)
# #
# # print("Successfully connected to: " + HOST)
# #
# # remote_connection = ssh_client.invoke_shell()
# # remote_connection.send("en\n")
# # remote_connection.send("config ter\n")
# # remote_connection.send("do sho run\n")
# # time.sleep(1)
# #
# # output = remote_connection.recv(6553)
# # print(output.decode('ascii'))
# #
# # ssh_client.close()
# def excute():
import paramiko
from flask import request
from flask_sqlalchemy import SQLAlchemy
import MySQLdb as mdb
import sys

from App import Devices

con = None
try:
    con = mdb.connect('localhost', 'root', 'root', 'crud')

    cur = con.cursor()

    # cur.execute("SET @ids := %s;")
    query = """SET @ids := %s;"""
    my_data = '3'
    tuple1 = (my_data)
    cur.execute(query, tuple1)
    cur.execute(
        "SELECT platform,name_platform,ipaddress_platform,password_platform,username_platform  FROM `crud`.`devices` WHERE id=@ids ;")

    ver = cur.fetchone()
    # ssh_client = paramiko.SSHClient()
    # ssh_client.connect(hostname='hostname', username=ver[3], password=ver[4])

    print(ver[1])

except mdb.Error as e:

    print("Error %d: %s" % (e.args[0], e.args[1]))
    sys.exit(1)

finally:

    if con:
        con.close()
