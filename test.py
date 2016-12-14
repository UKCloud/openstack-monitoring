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

"""
Connect to an OpenStack cloud.
For a full guide see TODO(etoews):link to docs on developer.openstack.org
"""

import argparse
import os

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
TEST_CLOUD = os.getenv('OS_TEST_CLOUD', 'cor00005')

class Opts(object):
    def __init__(self, cloud_name='cor00005', debug=False):
        self.cloud = cloud_name
        self.debug = debug
        # Use identity v3 API for examples.
        self.identity_api_version = '2'

def create_connection_from_config():
    opts = Opts(cloud_name=TEST_CLOUD)
    occ = os_client_config.OpenStackConfig()
    cloud = occ.get_one_cloud(opts.cloud)
    return connection.from_config(cloud_config=cloud, options=opts)

def list_servers(conn):
    print("List Servers:")

    for server in conn.compute.servers():
        print(server)


def list_images(conn):
    print("List Images:")

    for image in conn.compute.images():
        print(image)


def list_flavors(conn):
    print("List Flavors:")

    for flavor in conn.compute.flavors():
        print(flavor)


def list_keypairs(conn):
    print("List Keypairs:")

    for keypair in conn.compute.keypairs():
        print(keypair)

list_images(create_connection_from_config())
