import requests
import random
import json
import sys
import time


class QuerySaagieApi:
    def __init__(self, url_saagie, id_plateform, user, password):
        """
        Initialize the class
        Doc Saagie URL example: https://saagie-manager.prod.saagie.io/api/doc
        :param url_saagie: platform URL (eg: https://saagie-manager.prod.saagie.io)
        :param id_plateform: Platform Id (you can find in the URL when you are on your own
        platform (eg, the id of the platform is 6: https://saagie-beta.prod.saagie.io/manager/platform/6/#/manager/6))
        :param user: username to login with
        :param password: password to login with
        """
        if not url_saagie.endswith('/'):
            url_saagie += '/'
        self.url_saagie = url_saagie
        self.id_plateform = id_plateform
        self.suffix_api = 'api/v1/'
        self.auth = (user, password)

    def get_plateforms_info(self):
        """
        Getting information on all installed platform (eg: id, datamart IP, datamart Port, Datalake IP etC..c)
        requests.models.Response :return: the platforms informations
        """
        return requests.get(self.url_saagie + self.suffix_api + 'platform', auth=self.auth, verify=False)

    def get_plateform_info(self):
        """
        Getting information on a platform (eg: id, datamart IP, datamart Port, Datalake IP etC..c)
        requests.models.Response: return: platform informations
        """
        print(self.url_saagie + self.suffix_api + 'platform/' + str(self.id_plateform))
        return requests.get(self.url_saagie + self.suffix_api + 'platform/' + str(self.id_plateform)
                            , auth=self.auth
                            , verify=False)

    def get_impala_connection_info(self):
        """
        Getting information on a platform (eg: id, datamart IP, datamart Port, Datalake IP etC..c)
        requests.models.Response: return: platform informations
        """
        return requests.get(
            self.url_saagie + self.suffix_api + 'platform/' + str(self.id_plateform) + '/connectioninfo/impala'
            , auth=self.auth
            , verify=False)

    def get_plateform_env_vars(self):
        """
        Getting all environment variables available on the platform
        requests.models.Response: return: platform environment variables
        """
        return requests.get(self.url_saagie + self.suffix_api + 'platform/' + str(self.id_plateform) + '/envvars'
                            , auth=self.auth
                            , verify=False)

    def create_plateform_env_vars(self, name_envvar, value_envvar, is_password=False):
        """
        Create an environment variable
        string: param name_envvar: name of the environment variable
        string: param value_envvar: parameter of the environment variable
        requests.models.Response: return: status of the query (200: OK, other: KO -> available with
        method return_variable.status_code)
        """
        if is_password:
            the_password = 'true'
        else:
            the_password = 'false'

        payload = "{\"name\":\"" + str(name_envvar).upper() + '"' + \
                  ",\"value\":\"" + str(value_envvar) + '"' + \
                  ",\"isPassword\":" + the_password + \
                  ",\"platformId\":\"" + str(self.id_plateform) + '"}'

        return requests.post(self.url_saagie + self.suffix_api + 'platform/' + str(self.id_plateform) + '/envvars',
                             data=payload,
                             auth=self.auth,
                             verify=False)

    def delete_plateform_env_vars(self, id_venv):
        """
        Delete an environement variable environment variable
        int or string: param id_venv: id of the environment variable
        requests.models.Response: return: status of the query (200: OK, other: KO -> available with
        method return_variable.status_code)
        """
        return requests.delete(self.url_saagie + self.suffix_api + 'platform/' + str(self.id_plateform) + '/envvars/' \
                               + str(id_venv),
                               auth=self.auth,
                               verify=False)

    def run_job(self, job_id):
        """
        Run a job
        int or string:param job_id:
        requests.models.Response: return: status of the query (200: OK, other: KO -> available with
        method return_variable.status_code)
        """
        return requests.post(self.url_saagie + self.suffix_api + 'platform/' + str(self.id_plateform) + '/job/'
                             + str(job_id) + '/run',
                             auth=self.auth,
                             verify=False)

    def get_job_detail(self, job_id):
        """
        Get the status of a job
        int or string:param job_id:
        request.models.Response: return
        """
        return requests.get(self.url_saagie + self.suffix_api + 'platform/' + str(self.id_plateform) + '/job/' + str(job_id),
                            auth=self.auth,
                            verify=False)

    def run_job_callback(self, job_id, freq, timeout = -1):
        """
        Run a job and wait for the final status (KILLED, FAILED or SUCCESS)
        int or string:param job_id:
        int:param freq: Sec between two state ckecks
        int:param timeout: Sec before timeout
        string: return: the final state of this job
        """
        self.run_job(job_id)
        state = ''
        sec = 0
        to = False

        while(state != "STOPPED"):
            to = False if timeout == -1 else sec >= timeout
            if to:
                raise TimeoutError("Last state known : " + state)
            time.sleep(freq)
            sec += freq
            res = self.get_job_detail(job_id)
            state = json.loads(res.text)['last_state']['state']
            print('Current state : ' + state)

        return json.loads(res.text)['last_state']['lastTaskStatus'] 

    def __upload_file(self, file):
        """
        Private method to upload a file before create a job
        string: file: file path
        string: return: path to the file in SAAGIE
        """

        response = requests.post(
            self.url_saagie + self.suffix_api + 'platform/' + str(self.id_plateform) + "/job/upload",
            auth=self.auth,
            files={'file': open(file, 'rb')},
            verify=False)

        if response == -1:
            raise NameError("An unexpected error occured, please raise a ticket to SAAGIE to solve the problem")
        else:
            return json.loads(response.text)['fileName']

    def create_job(self, job_name, file, capsule_code='python', category='processing',
                   template="python {file} arg1 arg2", language_version='3.5.2', cpu=0.3,
                   memory=512, disk=512):
        """
        Create a job
        string: param job_name: job name
        string: param file: file path containing the code (only supporting .py file at the moment)
        string: param cpu: job's CPU
        int or string: param memory: job's Memory
        int or string: param disk: job's disk space
        requests.models.Response: return: status of the query (200: OK, other: KO -> available with
        method return_variable.status_code)
        """

        # Before creating a job you need to upload the file containing the code into SAAGIE
        fileName = self.__upload_file(file)

        # Building data needed in the requests.post method
        current = {
            "options": {"language_version": str(language_version)},
            "releaseNote": "",
            "template": str(template),
            "memory": str(memory),
            "cpu": str(cpu),
            "disk": str(disk),
            "file": str(fileName),
            "isInternalSubDomain": False,
            "isInternalPort": False
        }

        data = {
            "platform_id": str(self.id_plateform),
            "capsule_code": str(capsule_code),
            "category": str(category),
            "current": current,
            "always_email": False,
            "manual": True,
            "retry": "",
            "schedule": "R0/2019-02-27T09:51:11.607Z/P0Y0M1DT0H0M0S",
            "name": str(job_name)
        }

        # sending the request
        r = requests.post(self.url_saagie + self.suffix_api + 'platform/' + str(self.id_plateform) + "/job",
                          data=json.dumps(data),
                          auth=self.auth,
                          verify=False
                          )

        return r

    def create_pipeline(self, list_id_jobs):
        dict_workflow = {}
        dict_workflow['name'] = 'test_ap'
        list_worklfow = []
        position_job_workflow = 0
        for id in list_id_jobs:
            list_worklfow.append({"id": int(id), "position": position_job_workflow})
            position_job_workflow += 1
        dict_workflow['jobs'] = list_worklfow

        r = requests.post(self.url_saagie + self.suffix_api + 'platform/' + str(self.id_plateform) + "/workflow",
                          data=json.dumps(dict_workflow),
                          auth=self.auth,
                          verify=False
                          )
        return r