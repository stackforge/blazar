# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from climate.manager import exceptions
from climate import tests
from climate.utils.openstack import base


class TestBaseStackUtils(tests.TestCase):

    def setUp(self):
        super(TestBaseStackUtils, self).setUp()

        self.base = base

        self.service_type = 'fake_service'
        self.url = 'http://%s-net.com'

    def test_url_for_good_v3(self):
        #TODO(n.s.):Can't find v3 endpoint example. Fix it later.
        pass

    def test_url_for_good_v2_public(self):
        service_catalog = \
            [{"endpoints": [{"adminURL": self.url % 'admin',
                             "region": "RegionOne",
                             "internalURL": self.url % 'internal',
                             "publicURL": self.url % 'public'}],
              "type": "fake_service",
              "name": "foo"}]

        url = self.base.url_for(service_catalog, self.service_type)
        self.assertEqual(url, self.url % 'public')

    def test_url_for_good_v2_admin(self):
        service_catalog = \
            [{"endpoints": [{"adminURL": self.url % 'admin',
                             "region": "RegionOne",
                             "internalURL": self.url % 'internal',
                             "publicURL": self.url % 'public'}],
              "type": "fake_service",
              "name": "foo"}]

        url = self.base.url_for(service_catalog, self.service_type,
                                endpoint_interface='admin')
        self.assertEqual(url, self.url % 'admin')

    def test_url_for_no_service(self):
        service_catalog = \
            [{"endpoints": [{"adminURL": self.url % 'admin',
                             "region": "RegionOne",
                             "internalURL": self.url % 'internal',
                             "publicURL": self.url % 'public'}],
              "type": "foo_service",
              "name": "foo"}]

        self.assertRaises(exceptions.ServiceNotFound, self.base.url_for,
                          service_catalog, self.service_type)

    def test_url_for_no_endpoints(self):
        service_catalog = \
            [{"type": "fake_service",
              "name": "foo"}]

        self.assertRaises(exceptions.EndpointsNotFound, self.base.url_for,
                          service_catalog, self.service_type)
