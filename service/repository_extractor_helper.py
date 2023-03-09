import json
import time
from logging import Logger
import requests

from configurations.repository_extractor_helper_configurations import RepositoryExtractorHelperConfigurations


def get_configurations():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    return config


class RepositoryExtractorHelper:
    def __init__(self, logger: Logger, base_api_endpoint, headers):
        self.logger = logger
        self.base_api_endpoint = base_api_endpoint
        self.headers = headers
        config = get_configurations()
        helper_config = config["repository_extractor_helper"]
        self.configurations = RepositoryExtractorHelperConfigurations(helper_config["max_retries"], helper_config["sleep_time"])

    def get_repo_latest_releases(self):
        latest_releases_names = []
        releases_endpoint = "/releases"
        api_endpoint = self.base_api_endpoint + releases_endpoint
        retry_number = 0
        while retry_number < self.configurations.max_retries:
            try:
                response = requests.get(api_endpoint, headers=self.headers)
                if not response.status_code == 200:
                    raise requests.exceptions.HTTPError(f"the received status code is {response.status_code} from {self.base_api_endpoint}")
                latest_releases = json.loads(response.content)[:3]
                for release in latest_releases:
                    latest_releases_names.append(release["name"])
                return latest_releases_names

            except requests.exceptions.HTTPError as ex:
                extra_msg = f"exception is {str(ex)}, exception_type is {type(ex).__name__}"
                self.logger.error("an http error occurred during the api request", extra={"extra": extra_msg})

            except Exception as ex:
                extra_msg = f"exception is {str(ex)}, exception_type is {type(ex).__name__}"
                self.logger.error("an unexpected error occurred while trying to get repo latest releases",
                                  extra={"extra": extra_msg})
                retry_number += 1
                time.sleep(self.configurations.sleep_time)

    def get_number_of_repo_forks(self):
        retry_number = 0
        while retry_number < self.configurations.max_retries:
            try:
                response = requests.get(self.base_api_endpoint, headers=self.headers)
                if not response.status_code == 200:
                    raise requests.exceptions.HTTPError(f"the received status code is {response.status_code} from {self.base_api_endpoint}")
                return response.json()['forks_count']

            except requests.exceptions.HTTPError as ex:
                extra_msg = f"exception is {str(ex)}, exception_type is {type(ex).__name__}"
                self.logger.error("an http error occurred during the api request", extra={"extra": extra_msg})

            except Exception as ex:
                extra_msg = f"exception is {str(ex)}, exception_type is {type(ex).__name__}"
                self.logger.error("an unexpected error occurred while trying to get the number of repo forks",
                                  extra={"extra": extra_msg})
                retry_number += 1
                time.sleep(self.configurations.sleep_time)