import re
import sys

#vserver = input("Enter the name of the VServer you are looking for: ")
if len(sys.argv) is 2:
    vserver = sys.argv[1]
else:
    num_arguments = len(sys.argv) - 1
    sys.exit("You must include a single argument, you included: " + str(num_arguments))

if vserver :
    #print("#Looking for configuration for " + vserver)
    pass
else:
    sys.exit("You must enter a VServer.  Program aborted.")

with open("ns.conf") as f_config:
    show_run = f_config.readlines()

f_config.close()

vserver_config = []
vserver_regex = ".* vserver.*" + vserver.strip() + " .*"

for run_line in show_run:
    vserver_match = re.search(vserver_regex, run_line)
    if vserver_match is not None:
        vserver_config.append(vserver_match.group(0))

if vserver_config:
    pass
else:
    sys.exit("There were no matches for that VServer.  Program aborted.")

vserver_lb = False
for vserver_line in vserver_config:
    lb_match = re.search(r"add lb vserver", vserver_line)
    if lb_match:
        vserver_lb = True

if vserver_lb:
    pass
else:
    sys.exit("A Vserver was found but it is not a load balancer.  This script is still in development for other Vserver types.")

services_config = []
bind_regex = "^bind lb vserver " + vserver + " (.*)"

for vserver_line in vserver_config:
    bind_match = re.search(bind_regex, vserver_line)
    if bind_match is not None:
        service_regex = ".*service.* " + bind_match.group(1) + " .*"
        bind_lb_vserver_regex = "^bind lb vserver .* " + bind_match.group(1) + " .*"
        for run_line in show_run:
            service_match = re.search(service_regex, run_line)
            if service_match is not None:
                bind_lb_match = re.search(bind_lb_vserver_regex, service_match.group(0))
                if bind_lb_match is None:
                    services_config.append(service_match.group(0))
    else:
        bind_cs_vserver_regex = "^bind cs vserver " + vserver + " .*"
        bind_cs_match = re.search(bind_cs_vserver_regex, vserver_line)
        if bind_cs_match is not None:
            print(vserver_line)
            split_line = vserver_line.split()
            for key, split_item in enumerate(split_line):
                lbvserver_match = re.search("^-(|target)(lbv|LBV)server$", split_item, flags=re.IGNORECASE)
                if lbvserver_match is not None:
                    print(split_line[key + 1])
        else:
            #print("no match " + vserver_line)
            pass

if services_config:
    #print("#Found at least one service, finding servers.")
    pass
else:
    sys.exit("No services found.  Program aborted.")

servers_config = []

for service_line in services_config:
    add_service_match = re.search("add service .*", service_line)
    if add_service_match is not None:
        server_regex = "add server " + add_service_match.group(0).split()[3] + ".*"
        for run_line in show_run:
            server_match = re.search(server_regex, run_line)
            if server_match is not None:
                servers_config.append(server_match.group(0))

if servers_config:
    #print("#Found at least one server, completing.")
    pass
else:
    sys.exit("No servers found.  Program aborted.")

print("\n\n#Server config:")
for server_config_line in servers_config:
    print(server_config_line)

print("\n#Service config:")
for service_config_line in services_config:
    print(service_config_line)

print("\n#Vserver config:")
for vserver_config_line in vserver_config:
    print(vserver_config_line)
