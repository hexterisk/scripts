#!/usr/bin/python3
# coding=utf-8

import os
import sys
import subprocess

if __name__ == "__main__":

    # Credentials for remote server.
    remote_user =
    remote_ip =
    remote_db =
    remote_password =
    # Credentials for local server.
    local_user =
    local_db =
    local_password =
    # Ports are handled in ~/.ssh/config since we use OpenSSH

    print("\033[92m[+] Initiated table migration from {remote_db} for {remote_user}@{remote_ip} to {local_db} for {local_user}.\033[00m".format(remote_db = remote_db, remote_user = remote_user, remote_ip = remote_ip, local_db = local_db, local_user = local_user))

    # List of tables to be migrated.
    tables = []

    # Loop to iterate over tables to be migrated.
    for table in tables:

        print("\033[96m[~] Migrating table {table}.\033[00m".format(table = table))

        # Dump the table using a SSH channel.
        dumpCommand = "mysqldump -u {remote_user} -p {remote_db} {table} > {table}_dump.sql".format(remote_user = remote_user, remote_db = remote_db, table = table)
        dump = subprocess.Popen(["ssh", "{remote_user}@{remote_ip}".format(remote_user = remote_user, remote_ip = remote_ip), dumpCommand],
                                shell = False,
                                stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE)
        dump.stdin.write(remote_password.encode() + b'\n')
        result = dump.stdout.readlines()
        if result == []:
            print("\033[37m[+] Dumped table {table}.\033[00m".format(table = table))
            
            # Fetch the table dump using a SCP channel.
            copy = subprocess.Popen(["scp", "{remote_user}@{remote_ip}:{table}_dump.sql".format(remote_user = remote_user, remote_ip = remote_ip, table = table), "{table}_dump.sql".format(table = table)],
                                        shell = False,
                                        stdin = subprocess.PIPE,
                                        stdout = subprocess.PIPE,
                                        stderr = subprocess.PIPE)
            
            if copy.stdout.readlines() == []:
                if not os.path.exists("{table}_dump.sql".format(table = table)):
                    time.sleep(10)
                
                print("\033[37m[+] Fetched table {table}.\033[00m".format(table = table))
                delete = subprocess.Popen(["ssh", "{remote_user}@{remote_ip}".format(remote_user = remote_user, remote_ip = remote_ip), "rm -rf {table}_dump.sql".format(table = table)],
                                        shell = False,
                                        stdin = subprocess.PIPE,
                                        stdout = subprocess.PIPE,
                                        stderr = subprocess.PIPE)
                push = subprocess.Popen(["mysql", "-u", "{local_user}".format(local_user = local_user), "-p", "{local_db}".format(local_db = local_db), "<", "{table}_dump.sql".format(table = table)],
                                        shell = False,
                                        stdin = subprocess.PIPE,
                                        stdout = subprocess.PIPE,
                                        stderr = subprocess.PIPE)
                push.stdin.write(local_password.encode() + b'\n')
                os.remove("{table}_dump.sql".format(table = table))
                print("\033[92m[+] Table {table} pushed into the local database.\033[00m".format(table = table))
            else:
                print("\033[91m[!] Error fetching the file. It does not exist.\033[00m")
                continue
        else:
            print("\033[91m[!] Error dumping table.\033[00m")
            
    print("\033[92m[+] Tables migrated from remote database to local database successfully.\033[00m")
