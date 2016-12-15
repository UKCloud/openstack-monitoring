# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import argparse
import os
import time
import json

import os_client_config

from openstack import connection
from openstack import profile
from openstack import utils
import sys

utils.enable_logging(True, stream=sys.stdout)

#: Defines the OpenStack Client Config (OCC) cloud key in your OCC config
#: file, typically in $HOME/.config/openstack/clouds.yaml. That configuration
#: will determine where the examples will be run and what resource defaults
#: will be used to run the examples.
CLOUD_NAME = 'cor00005'
TEST_CLOUD = os.getenv('OS_TEST_CLOUD', CLOUD_NAME)
SERVER_NAME = 'openstacksdk-example'
IMAGE_NAME = 'CentOS 7'
FLAVOR_NAME = 'm1.small'
NETWORK_NAME = 'NetworkTest'

class Opts(object):
    def __init__(self, cloud_name=CLOUD_NAME, debug=False):
        self.cloud = cloud_name
        self.debug = False
        self.identity_api_version = '3'

def create_connection_from_config():
    opts = Opts(cloud_name=TEST_CLOUD)
    occ = os_client_config.OpenStackConfig()
    cloud = occ.get_one_cloud(opts.cloud)
    return connection.from_config(cloud_config=cloud, options=opts)

def create_server(conn):
    print("Create Server:")

    image = conn.compute.find_image(IMAGE_NAME)
    flavor = conn.compute.find_flavor(FLAVOR_NAME)
    network = conn.network.find_network(NETWORK_NAME)
    results = {}

    start_time = time.time()
    server = conn.compute.create_server(
        name=SERVER_NAME, image_id=image.id, flavor_id=flavor.id,
        networks=[{"uuid": network.id}])
    server = conn.compute.wait_for_server(server)

    taskTime = time.time() - start_time

    results['task_name'] = 'create server'
    results['time'] = taskTime
    file = open('/var/www/html/server-creation', 'w')
    file.write(json.dumps(results))
    delete_server(conn, server)


def delete_server(conn, server):
    print("Delete Server:")

    conn.compute.delete_server(server)

conn = create_connection_from_config()
server = create_server(conn)
