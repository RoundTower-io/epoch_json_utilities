

import os
import requests
import pprint

api_key = os.environ['EPOCH_KEY']

BASE_URL = 'https://uopx.epoch.nutanix.com/'

def get_collector_list():

    global BASE_URL
    r = requests.get(url=str(BASE_URL + "sp-lb/collector-list"),
                     headers={"x-app-key": api_key})
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        raise Exception("get collector list rc=%d" % r.status_code)


def get_single_collector_info(collector_id):
    global BASE_URL
    r = requests.get(url=str(BASE_URL + "sp-lb/single-collector-info/collector/" + collector_id),
                     headers={"x-app-key": api_key})
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        raise Exception("get single collector info rc=%d" % r.status_code)


def get_collector_id_from_host_name(hostname):
    list = get_collector_list()
    for host in list["collector_list"]:
        if str(host["host_name"]).lower() == str(hostname).lower():
            return host["id"]
    return -1


def get_host_name_from_collector_id(collector_id):
    list = get_collector_list()
    for host in list["collector_list"]:
        if str(host["id"]).lower() == str(collector_id).lower():
            return host["host_name"]
    return -1


#resp = get_collector_list()

#print(len(resp["collector_list"]))
#for host in resp["collector_list"]:
#    print("host " + host['host_name'])

#pprint.pprint(resp)

cid = get_collector_id_from_host_name('ac-00086689')

single = get_single_collector_info(cid)

pprint.pprint(single)

