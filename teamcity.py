import requests
import base64
import fire
import json

user = 'user'
password = 'password'  # base64 encoded
host = 'http://teamcity.host:8111/'


class teamcity(object):
    def list_projects(self, project_id='MP_APP'):
        url = host + "app/rest/projects/id:{!s}".format(project_id)
        r = requests.get(
            url,
            auth=(user, base64.b64decode(password).decode('utf-8')),
            headers={'accept': 'application/json'})
        the_dict = json.loads(r.text)
        return the_dict

if __name__ == '__main__':
    fire.Fire(teamcity)
