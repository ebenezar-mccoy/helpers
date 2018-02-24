#!env python3
import os
import sys
import yaml
import json
import re
import glob
from pathlib import Path

magic_list = {
    'data': []
}


class AppDiscovery:
    """Zabbix autodiscovery module for application monitoring."""

    def __init__(self, app_type=None, app_location=None):
        """Everything starts here."""
        self.app_type = sys.argv[1] if sys.argv[1] else False
        self.app_location = sys.argv[2] if sys.argv[2] else False
        self.get_data()
        print(json.dumps(magic_list, indent=4))

    def get_data(self):
        """Selector for specific application type."""
        if self.app_type == 'spring':
            self.get_spring_data()
        elif self.app_type == 'tomcat':
            self.get_tomcat_data()

    def get_spring_data(self):
        """Spring applications."""
        for file in os.listdir(self.app_location):
            if file.startswith('event') or file.endswith('service'):
                conf_dir = os.path.join(self.app_location, file + '/')
                conf = yaml.load(Path(glob.glob(
                    conf_dir + '*.yaml')[0]).read_text())
                magic_list["data"].append(
                    ({
                        '{#APP_NAME}': file,
                        '{#APP_PORT_TOMCAT}': conf['server']['port'],
                        '{#APP_TITAN_URL}': re.search(
                            '://(.*);',
                            conf['datasource']['titan']['url']).group(1),
                        '{#JAR_FILE}': glob.glob(conf_dir + '*.jar')[0]
                    }))

    def get_tomcat_data(self):
        """Tomcat applications."""
        for file in os.listdir(self.app_location):
            if file.endswith('war'):
                magic_list['data'].append(
                    ({
                        '{#APP_NAME}': file,
                        '{#APP_PORT_TOMCAT}': '8080',
                        '{#JAR_FILE}': self.app_location + '/' + file
                    }))


if __name__ == '__main__':
    AppDiscovery()
