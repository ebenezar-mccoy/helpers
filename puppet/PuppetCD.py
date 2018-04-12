#!env python3
import requests
import json
import yaml
import re
import sys

artifacts = [
    ['com.cinemacity', 'test-app', 'jar'],
]

try:
    file = sys.argv[1]
except IndexError:
    file = '/tmp/artifacts.yaml'

host = 'http://some.host:8081/nexus/service/local/'

PuppetDB = {
    'MASTER': {},
    'DEVELOPMENT': {},
    'RELEASE': {},
    'HOTFIX': {}
}

"""We don't use yaml aliases."""
noalias = yaml.dumper.SafeDumper
noalias.ignore_aliases = lambda self, data: True


class PuppetCD:
    """Artifacts databsae builder for puppet deployments."""

    def generate_db(artifact_branch, artifact):
        """Generate puppet database."""
        dest_artifact = {}
        data = PuppetCD.get_artifact_information(artifact_branch,
                                                 artifact)['data']
        if data:
            if 'baseVersion' in data:
                version = data['baseVersion']
            else:
                version = data['version']
            dest_artifact['gav'] = "{!s}:{!s}:{!s}:{!s}".format(
                data['groupId'],
                data['artifactId'],
                version,
                data['extension'])
            dest_artifact['version'] = data['version']
            dest_artifact['sha1'] = data['sha1']
            dest_artifact['suffix'] = data['repo']
            PuppetDB[artifact_branch][artifact[1]] = PuppetCD.write_latest(
                artifact[1], artifact_branch, dest_artifact)

    def get_artifact_information(artifact_branch, artifact):
        """Get information about artifact."""
        gav, name, extension = artifact[0], artifact[1], artifact[2]
        repo, version = PuppetCD.return_repo_and_version(gav,
                                                         name, artifact_branch)
        url = host + "artifact/maven/resolve?r={!s}&g={!s}&a={!s}&p={!s}"\
                     "&v={!s}".format(repo, gav, name, extension, version)
        response = requests.get(url, headers={'accept': 'application/json'})
        try:
            artifact = json.loads(response.text)
            artifact['data']['repo'] = repo
        except ValueError:
            artifact = {"data": {}}
        return artifact

    def write_latest(artifact_name, artifact_branch, dest_artifact):
        """Chose latest artifact."""
        artifact = dest_artifact
        current_version = artifact['version'].split('-')[0]
        if ((artifact_branch == 'HOTFIX' or artifact_branch == 'RELEASE') and
           artifact_name in PuppetDB['MASTER']):
                if current_version <= PuppetDB['MASTER'][artifact_name]['version']:
                    artifact = PuppetDB['MASTER'][artifact_name]
        return artifact

    def return_repo_and_version(gav, name, branch):
        """Return nexus repository and version."""
        if branch == 'MASTER':
            list = ['releases', 'RELEASE']
        if branch == 'DEVELOPMENT':
            list = ['snapshots', 'LATEST']
        if branch == 'HOTFIX' or branch == 'RELEASE':
            repo = 'rc'
            version = PuppetCD.select_release_or_hotfix(gav, name, branch)
            if not version:
                repo = 'releases'
                version = 'RELEASE'
            list = [repo, version]
        return list

    def select_release_or_hotfix(gav, name, branch):
        """Select latest release or hotfix version."""
        version = []
        url = host + "repositories/rc/content/"\
            "{!s}/{!s}/".format(gav.replace('.', '/'), name)
        response = requests.get(url, headers={'accept': 'application/json'})
        try:
            versions = json.loads(response.text)
        except ValueError:
            versions = {"data": {}}
        for x in versions['data']:
            if (re.match("^\d+\.\d+\.\d+\-SNAPSHOT", x['text']) and
                    branch == 'RELEASE'):
                version.append(x['text'].strip('-SNAPSHOT'))
            if (re.match("^\d+\.\d+\.\d+\.\d+\-SNAPSHOT", x['text']) and
                    branch == 'HOTFIX'):
                version.append(x['text'].strip('-SNAPSHOT'))
        if version:
            version.sort(key=lambda s: list(map(int, s.split('.'))))
            version = version[-1] + '-SNAPSHOT'
            return version


def main():
    """Evrything starts here."""
    print('working:')
    for art in artifacts:
        for art_branch in PuppetDB:
            PuppetCD.generate_db(art_branch, art)
            print('.', end='', flush=True)
    print('ok')
    DB = {}
    DB['ccdev::deployments::versions'] = PuppetDB
    # print(yaml.dump(DB, default_flow_style=False, Dumper=noalias))
    with open(file, 'w') as outfile:
        yaml.dump(DB, outfile, default_flow_style=False, Dumper=noalias)


if __name__ == '__main__':
    main()
