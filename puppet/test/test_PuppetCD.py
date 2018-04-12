#!env python3
import unittest
import requests_mock
from PuppetCD import *
from test.mocks import *

artifacts = [
    ['com.cinemacity', 'no-app', 'war'],
    ['com.cinemacity', 'app-1', 'war'],
    ['com.cinemacity', 'app-2', 'war'],
    ['com.cinemacity', 'app-3', 'war'],
    ['com.cinemacity', 'app-4', 'war'],
    ['com.cinemacity', 'app-5', 'war'],
    ['com.cinemacity', 'app-6', 'war'],
    ['com.cinemacity', 'app-7', 'war'],
    ['com.cinemacity', 'app-8', 'war'],
    ['com.cinemacity', 'app-9', 'war']
]


class TestPuppetCD(unittest.TestCase):
    @classmethod
    @requests_mock.mock()
    def setUpClass(self, m):
        for mock in r_mock:
            url = nexus + mock[0]
            m.get(url, text=mock[1])
        for art in artifacts:
            for art_branch in PuppetDB:
                PuppetCD.generate_db(art_branch, art)
        print(yaml.dump(PuppetDB, default_flow_style=False, Dumper=noalias))

    def test_no_app_in_nexus(self):
        for branch in ['DEVELOPMENT', 'MASTER', 'RELEASE', 'HOTFIX']:
            self.assertNotIn('no-app', PuppetDB[branch])

    def test_app_only_in_snapshots(self):
        for branch in ['MASTER', 'RELEASE', 'HOTFIX']:
            self.assertNotIn('app-1', PuppetDB[branch])
        self.assertEqual(PuppetDB['DEVELOPMENT']['app-1']['gav'],
                         'com.cinemacity:app-1:1.1.1-SNAPSHOT:war')

    def test_app_only_in_releases(self):
        self.assertNotIn('app-2', PuppetDB['DEVELOPMENT'])
        for branch in ['MASTER', 'RELEASE', 'HOTFIX']:
            self.assertEqual(PuppetDB[branch]['app-2']['gav'],
                             'com.cinemacity:app-2:2.2.2:jar')

    def test_app_only_in_rc_hotfix(self):
        for branch in ['DEVELOPMENT', 'MASTER', 'RELEASE']:
            self.assertNotIn('app-3', PuppetDB[branch])
        self.assertEqual(PuppetDB['HOTFIX']['app-3']['gav'],
                         'com.cinemacity:app-3:3.3.3.3-SNAPSHOT:war')

    def test_app_only_in_rc_releases(self):
        for branch in ['DEVELOPMENT', 'MASTER', 'HOTFIX']:
            self.assertNotIn('app-4', PuppetDB[branch])
        self.assertEqual(PuppetDB['RELEASE']['app-4']['gav'],
                         'com.cinemacity:app-4:4.4.4-SNAPSHOT:war')

    def test_latest_selector_from_rc(self):
        for branch in ['DEVELOPMENT', 'MASTER']:
            self.assertNotIn('no-app', PuppetDB[branch])
        self.assertEqual(PuppetDB['HOTFIX']['app-5']['gav'],
                         'com.cinemacity:app-5:5.5.5.2-SNAPSHOT:war')
        self.assertEqual(PuppetDB['RELEASE']['app-5']['gav'],
                         'com.cinemacity:app-5:5.5.2-SNAPSHOT:war')

    def test_master_newer_then_rc(self):
        self.assertNotIn('app-6', PuppetDB['DEVELOPMENT'])
        for branch in ['MASTER', 'RELEASE', 'HOTFIX']:
            self.assertEqual(PuppetDB['HOTFIX']['app-6']['gav'],
                             'com.cinemacity:app-6:6.1.2:jar')

    def test_master_older_then_rc(self):
        self.assertNotIn('app-7', PuppetDB['DEVELOPMENT'])
        self.assertEqual(PuppetDB['HOTFIX']['app-7']['gav'],
                         'com.cinemacity:app-6:7.1.1.1-SNAPSHOT:war')
        self.assertEqual(PuppetDB['RELEASE']['app-7']['gav'],
                         'com.cinemacity:app-6:7.1.2-SNAPSHOT:war')
        self.assertEqual(PuppetDB['MASTER']['app-7']['gav'],
                         'com.cinemacity:app-7:7.1.1:jar')

    def test_release_eq_rc_hotfix(self):
        self.assertNotIn('app-8', PuppetDB['DEVELOPMENT'])
        for branch in ['MASTER', 'RELEASE', 'HOTFIX']:
            self.assertEqual(PuppetDB['HOTFIX']['app-8']['gav'],
                             'com.cinemacity:app-8:8.1.1:jar')

    def test_release_eq_rc(self):
        self.assertNotIn('app-9', PuppetDB['DEVELOPMENT'])
        for branch in ['MASTER', 'RELEASE', 'HOTFIX']:
            self.assertEqual(PuppetDB['HOTFIX']['app-9']['gav'],
                             'com.cinemacity:app-9:9.1.1.1:jar')
