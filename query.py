"""
This is the calling script for the epoch library
"""
import epoch
import json
import pprint

resp = epoch.get_collector_list()
no_tags = []
no_host = 0
no_os = []
os_undefined = []
hosts_total = 0
for host in resp["collector_list"]:
    hosts_total += 1
    if host["host_name"]:
        print(str(host["host_name"]) + ": ", end='', flush=True)
    else:
        print("------------>No hostname field in structure")
        pprint.pprint(host)
        no_host += 1
        continue

    tags = epoch.get_api_tags(host["host_name"])
    if tags:
        dtags = tags[0]
        if "appdb_os_release" in dtags["tags"]:
            if str(dtags["tags"]["appdb_os_release"]) == "undefined":
                os_undefined.append(host["host_name"])
            print(str(dtags["tags"]["appdb_os_release"]))
        else:
            print("No OS Release Defined!")
            no_os.append(host["host_name"])
    else:
        print("-----------> NO tags returned")
        no_tags.append(host["host_name"])

print("Total hosts: " + str(hosts_total))
print("Missing hostname total: " + str(no_host))
print("Missing tags total: " + str(len(no_tags)))
print("Missing OS: " + str(len(no_os)))
print("Undefined OS: " + str(len(os_undefined)))

with open('no_tags.json', 'w') as g:
    json.dump(no_tags, g)

with open('no_os.json', 'w') as h:
    json.dump(no_os, h)

with open('os_undefined.json', 'w') as i:
    json.dump(os_undefined, i)

