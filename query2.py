import epoch
import pprint
import json

json_topo = """
{
  "groupby": [
    "tags.appdb_os_release"
  ],
  "filter": {
    "type": "all_values",
    "value": {
      "text": ""
    },
    "key": "host_name"
  },
  "enable_one_hop": true,
  "one_hop_groupby": [],
  "interval": [
    1561957201000,
    1564635601000
  ]
}
"""
data = json.loads(json_topo)
topo = epoch.post_topology(data)
pprint.pprint(topo)
