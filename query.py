"""
This is the calling script for the epoch library
"""
import epoch

resp = epoch.get_collector_list()

#print(len(resp["collector_list"]))
for host in resp["collector_list"]:
    cid = epoch.get_collector_id_from_host_name(host["host_name"], resp)
    single = epoch.get_single_collector_info(cid)
    print(str(host["host_name"]) + " " + str(single["metadata"]["tags"]))

# for role in ["dev", "qa", "prod"]:
#     hosts = get_hosts_for_env(role)
#     print(role + " hosts: " + str(len(hosts)))


# resp = get_collector_list()
# for host in resp["collector_list"]:
#     print("host: " + str(host["host_name"]))
#     pprint.pprint(get_api_tags(host["host_name"]))



#pprint.pprint(get_api_tags_paginated(5000, 1))
