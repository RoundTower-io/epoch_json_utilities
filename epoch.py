"""
This is an API wrapper library for Nutanix's Epoch tool.

"""

import os
import requests
import logging
import http.client as http_client
import json

EPOCH_KEY = os.environ['EPOCH_KEY']
EPOCH_URL = os.environ['EPOCH_URL']


# https://uopx.epoch.nutanix.com/

#
# API Wrappers
#
def get_collector_list():
    """
    A simple wrapper for the "sp-lb/collector-list" REST API described here:
    https://app.swaggerhub.com/apis-docs/nutanix-epoch/epoch/1.12.20#/collectors/collectorList
    :return: The output of the API call
    """
    global EPOCH_URL, EPOCH_KEY
    r = requests.get(url=str(EPOCH_URL + "sp-lb/collector-list"),
                     headers={"x-app-key": EPOCH_KEY})
    if r.status_code == requests.codes.ok:
        return r.json()
    raise Exception("get collector list rc=%d" % r.status_code)


def get_single_collector_info(collector_id):
    """
    A simple wrapper for the "sp-lb/single-collector-info/collector/" REST API described here:
    https://app.swaggerhub.com/apis-docs/nutanix-epoch/epoch/1.12.20#/collectors/singleCollectorInfoByCollectorId

    :param collector_id: The collector (host) ID
    :return: Detailed information about the host
    """
    global EPOCH_URL, EPOCH_KEY
    r = requests.get(url=str(EPOCH_URL + "sp-lb/single-collector-info/collector/" + collector_id),
                     headers={"x-app-key": EPOCH_KEY})
    if r.status_code == requests.codes.ok:
        return r.json()
    raise Exception("get single collector info rc=%d" % r.status_code)


def get_api_tags(hostname):
    """
    Get the tags associated with a host name

    :param hostname:  The host name
    :return: JSON structure containing the tag information
    """
    global EPOCH_URL, EPOCH_KEY
    r = requests.get(url=str(EPOCH_URL + "api/v1/tags/hosts/" + hostname),
                     headers={"x-app-key": EPOCH_KEY})
    if r.status_code == requests.codes.ok:
        return r.json()
    raise Exception("Get API tags rc=%d" % r.status_code)


def get_all_api_tags_paginated(pagesize, pagenumber):
    """
    Get all the API tags for all hosts in a paginated format
    :param pagesize: Integer page size
    :param pagenumber: The page number
    :return: A JSON struct with the tag information for each host
    """
    global EPOCH_URL, EPOCH_KEY
    r = requests.get(url=str(EPOCH_URL + "api/v1/tags/hosts/" + str(pagesize) + "/" + str(pagenumber)),
                     headers={"x-app-key": EPOCH_KEY})
    if r.status_code == requests.codes.ok:
        return r.json()
    raise Exception("Get API tags paginated rc=%d" % r.status_code)


def get_topology_maps():
    global EPOCH_URL, EPOCH_KEY
    r = requests.get(url=str(EPOCH_URL + "auth-api/topology-map"),
                     headers={"x-app-key": EPOCH_KEY})
    if r.status_code == requests.codes.ok:
        return r.json()
    raise Exception("Get topology maps rc=%d" % r.status_code)


def get_one_topology_map(topology_map_id):
    global EPOCH_URL, EPOCH_KEY
    r = requests.get(url=str(EPOCH_URL + "auth-api/topology-map/" + topology_map_id),
                     headers={"x-app-key": EPOCH_KEY})
    if r.status_code == requests.codes.ok:
        return r.json()
    raise Exception("Get one topology map rc=%d" % r.status_code)


def post_topology(epoch_filter):
    global EPOCH_URL, EPOCH_KEY
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain', "x-app-key": EPOCH_KEY}

    r = requests.post(url=str(EPOCH_URL + "api/v3/topology"),
                      data=json.dumps(epoch_filter),
                      headers=headers)
    if r.status_code == requests.codes.ok:
        return r.json()
    raise Exception("Get topology rc=%d" % r.status_code)


#
#
# Ancillary functions
#
def get_collector_id_from_host_name(hostname, list):
    """
    Given a host name, return a collector ID

    :param hostname: The host name
    :param list: The collector list
    :return: The ID
    """
    for host in list["collector_list"]:
        if str(host["host_name"]).lower() == str(hostname).lower():
            return host["id"]
    return -1


def get_host_name_from_collector_id(collector_id, list):
    """
    Given a collector ID, return a host name

    :param collector_id:
    :param list: The collector list
    :return: The host name
    """
    for host in list["collector_list"]:
        if str(host["id"]).lower() == str(collector_id).lower():
            return host["host_name"]
    return -1


def get_total_host_count():
    """
    Get the total number of hosts defined
    :return: The count
    """
    resp = get_collector_list()
    return len(resp["collector_list"])


def get_hosts_for_env(env):
    """
    Get the total number of hosts for a given environment (dev, qa, prod).

    :param env: The environment type (dev, qa, prod)
    :return: A list of hosts for that environment
    """
    env_list = []
    resp = get_collector_list()
    for host in resp["collector_list"]:
        cid = get_collector_id_from_host_name(host["host_name"], resp)
        single = get_single_collector_info(cid)
        if "metadata" in single:
            tags = single["metadata"]["tags"]
            if "env" in tags and tags["env"] == env:
                env_list.append(host["host_name"])
        else:
            print("NO METADATA:" + host["host_name"])
    return env_list
