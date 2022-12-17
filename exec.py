import paramiko

router_ip = "192.168.5.11"
router_username = "alisfactory"
router_password = "Ad56#33n$xw3"

ssh = paramiko.SSHClient()

# Load SSH host keys.
ssh.load_system_host_keys()
# Add SSH host key automatically if needed.
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Connect to router using username/password authentication.
ssh.connect(router_ip,
            username=router_username,
            password=router_password,
            look_for_keys=False)

# Run command.
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("show int status")

output = ssh_stdout.readlines()
# Close connection.
ssh.close()

# Analyze show ip route output
for line in output:
    if "" in line:
        print("Found default route:")
        print(line)

# ------------------------------------------------------------------------------
# import paramiko
# import getpass
# import time
#
#
# HOST = 'HOSTADDR'
# user = 'user'
# password = 'password'
#
# ssh_client = paramiko.SSHClient()
# ssh_client = set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh_client.connect(host=HOST, username=user, password=password)
#
# print("Successfully connected to: " + HOST)
#
# remote_connection = ssh_client.invoke_shell()
# remote_connection.send("en\n")
# remote_connection.send("config ter\n")
# remote_connection.send("{{command}}\n")
# time.sleep(1)
#
# output = remote_connection.recv(6553)
# print(output.decode('ascii'))
#
# ssh_client.close()
