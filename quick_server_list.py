import re
import sys

with open("ns.conf") as f_config:
    show_run = f_config.readlines()

f_config.close()

print("#Finding list of load balancer vservers")
vserver_regex = "add lb vserver (\S*) .*"

for run_line in show_run:
    vserver_match = re.search(vserver_regex, run_line)
    if vserver_match is not None:
        print(vserver_match.group(1))

print("\n\n#Finding list of content switch vservers")
vserver_regex = "add cs vserver (\S*) .*"

for run_line in show_run:
    vserver_match = re.search(vserver_regex, run_line)
    if vserver_match is not None:
        print(vserver_match.group(1))

print("\n\n#Finding list of vpn vservers")
vserver_regex = "add vpn vserver (\S*) .*"

for run_line in show_run:
    vserver_match = re.search(vserver_regex, run_line)
    if vserver_match is not None:
        print(vserver_match.group(1))

print("\n\n#Finding list of authentication vservers")
vserver_regex = "add authentication vserver (\S*) .*"

for run_line in show_run:
    vserver_match = re.search(vserver_regex, run_line)
    if vserver_match is not None:
        print(vserver_match.group(1))

print("\n\n#Finding list of GSLB vservers")
vserver_regex = "add gslb vserver (\S*) .*"

for run_line in show_run:
    vserver_match = re.search(vserver_regex, run_line)
    if vserver_match is not None:
        print(vserver_match.group(1))
