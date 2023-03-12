import json
import time
from http import HTTPStatus
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
        self.configurations = RepositoryExtractorHelperConfigurations(helper_config["max_retries"],
                                                                      helper_config["sleep_time_between_retries"])

    def get_repo_latest_releases(self) -> list or None:
        latest_releases_names = []
        releases_endpoint = "/releases"
        api_endpoint = self.base_api_endpoint + releases_endpoint
        retry_number = 0
        while retry_number < self.configurations.max_retries:
            try:
                response = requests.get(api_endpoint, headers=self.headers)
                if response.status_code != HTTPStatus.OK:
                    raise requests.exceptions.HTTPError(f"bad status code from {self.base_api_endpoint}", response.status_code)
                latest_releases = json.loads(response.content)[:3]
                for release in latest_releases:
                    latest_releases_names.append(release["name"])
                return latest_releases_names

            except requests.exceptions.HTTPError as ex:
                extra_msg = f"exception is {str(ex)}, exception_type is {type(ex).__name__}"
                self.logger.warning("an http error occurred during the api request", extra={"extra": extra_msg})
                status_code = ex.args[1]
                if status_code >= 500:
                    retry_number += 1
                    time.sleep(self.configurations.sleep_time_between_retries)
                else:
                    break

            except Exception as ex:
                extra_msg = f"exception is {str(ex)}, exception_type is {type(ex).__name__}"
                self.logger.error("an unexpected error occurred while trying to get repo latest releases",
                                  extra={"extra": extra_msg})
                break

        if retry_number == self.configurations.max_retries:
            self.logger.error("failed to execute the api request successfully after retries")

    def get_number_of_repo_forks(self) -> int or None:
        retry_number = 0
        while retry_number < self.configurations.max_retries:
            try:
                response = requests.get(self.base_api_endpoint, headers=self.headers)
                if response.status_code != HTTPStatus.OK:
                    raise requests.exceptions.HTTPError(f"bad status code from {self.base_api_endpoint}", response.status_code)
                return response.json()['forks_count']

            except requests.exceptions.HTTPError as ex:
                extra_msg = f"exception is {str(ex)}, exception_type is {type(ex).__name__}"
                self.logger.warning("an http error occurred during the api request", extra={"extra": extra_msg})
                status_code = ex.args[1]
                if status_code >= 500:
                    retry_number += 1
                    time.sleep(self.configurations.sleep_time_between_retries)
                else:
                    break

            except Exception as ex:
                extra_msg = f"exception is {str(ex)}, exception_type is {type(ex).__name__}"
                self.logger.error("an unexpected error occurred while trying to get the number of repo forks",
                                  extra={"extra": extra_msg})
                break

        if retry_number == self.configurations.max_retries:
            self.logger.error("failed to execute the api request successfully after retries")

    def get_number_of_repo_stars(self) -> int or None:
        retry_number = 0
        while retry_number < self.configurations.max_retries:
            try:
                response = requests.get(self.base_api_endpoint, headers=self.headers)
                if response.status_code != HTTPStatus.OK:
                    raise requests.exceptions.HTTPError(f"bad status code from {self.base_api_endpoint}", response.status_code)
                return response.json()['stargazers_count']

            except requests.exceptions.HTTPError as ex:
                extra_msg = f"exception is {str(ex)}, exception_type is {type(ex).__name__}"
                self.logger.warning("an http error occurred during the api request", extra={"extra": extra_msg})
                status_code = ex.args[1]
                if status_code >= 500:
                    retry_number += 1
                    time.sleep(self.configurations.sleep_time_between_retries)
                else:
                    break

            except Exception as ex:
                extra_msg = f"exception is {str(ex)}, exception_type is {type(ex).__name__}"
                self.logger.error("an unexpected error occurred while trying to get the number of repo stars",
                                  extra={"extra": extra_msg})
                break

        if retry_number == self.configurations.max_retries:
            self.logger.error("failed to execute the api request successfully after retries")

    def get_repo_contributors(self) -> list or None:
        page = 1
        max_bulk_size = 100
        contributors = []
        retry_number = 0
        while True:
            if not retry_number < self.configurations.max_retries:
                break
            contributors_endpoint = f"/contributors?page={page}&per_page={max_bulk_size}"
            api_endpoint = self.base_api_endpoint + contributors_endpoint
            try:
                response = requests.get(api_endpoint, headers=self.headers)
                if response.status_code != HTTPStatus.OK:
                    raise requests.exceptions.HTTPError(f"bad status code from {self.base_api_endpoint}", response.status_code)
                contributors_bulk = response.json()
                contributors.extend(contributors_bulk)
                if len(contributors_bulk) == max_bulk_size:
                    page += 1
                    continue
                else:
                    return contributors

            except requests.exceptions.HTTPError as ex:
                extra_msg = f"exception is {str(ex)}, exception_type is {type(ex).__name__}"
                self.logger.warning("an http error occurred during the api request", extra={"extra": extra_msg})
                status_code = ex.args[1]
                if status_code >= 500:
                    retry_number += 1
                    time.sleep(self.configurations.sleep_time_between_retries)
                else:
                    break

            except Exception as ex:
                extra_msg = f"exception is {str(ex)}, exception_type is {type(ex).__name__}"
                self.logger.error("an unexpected error occurred while trying to get repo contributors",
                                  extra={"extra": extra_msg})
                break

        if retry_number == self.configurations.max_retries:
            self.logger.error("failed to execute the api request successfully after retries")

    def get_repo_pull_requests(self) -> list or None:
        page = 1
        max_bulk_size = 100
        pulls_requests = []
        retry_number = 0
        while True:
            if not retry_number < self.configurations.max_retries:
                break
            pulls_endpoint = f"/pulls?page={page}&per_page={max_bulk_size}"
            api_endpoint = self.base_api_endpoint + pulls_endpoint
            try:
                response = requests.get(api_endpoint, headers=self.headers)
                if not response.status_code == 200:
                    raise requests.exceptions.HTTPError(f"bad status code from {self.base_api_endpoint}", response.status_code)
                pulls_requests_bulk = response.json()
                pulls_requests.extend(pulls_requests_bulk)
                if len(pulls_requests_bulk) == max_bulk_size:
                    page += 1
                    continue
                else:
                    return pulls_requests

            except requests.exceptions.HTTPError as ex:
                extra_msg = f"exception is {str(ex)}, exception_type is {type(ex).__name__}"
                self.logger.warning("an http error occurred during the api request", extra={"extra": extra_msg})
                status_code = ex.args[1]
                if status_code >= 500:
                    retry_number += 1
                    time.sleep(self.configurations.sleep_time_between_retries)
                else:
                    break

            except Exception as ex:
                extra_msg = f"exception is {str(ex)}, exception_type is {type(ex).__name__}"
                self.logger.error("an unexpected error occurred while trying to get repo pull requests",
                                  extra={"extra": extra_msg})
                break

        if retry_number == self.configurations.max_retries:
            self.logger.error("failed to execute the api request successfully after retries")

    def get_number_of_repo_commits(self) -> int or None:
        page = 1
        max_bulk_size = 100  # the maximum amount of returned commits from a single api call.
        commits = []
        retry_number = 0
        while True:
            if not retry_number < self.configurations.max_retries:
                break
            commits_endpoint = f"/commits?page={page}&per_page={max_bulk_size}"
            api_endpoint = self.base_api_endpoint + commits_endpoint
            try:
                response = requests.get(api_endpoint, headers=self.headers)
                if not response.status_code == 200:
                    raise requests.exceptions.HTTPError(f"bad status code from {self.base_api_endpoint}", response.status_code)
                commits_bulk = response.json()
                commits.extend(commits_bulk)
                if len(commits_bulk) == max_bulk_size:
                    page += 1
                    continue
                else:
                    return len(commits)

            except requests.exceptions.HTTPError as ex:
                extra_msg = f"exception is {str(ex)}, exception_type is {type(ex).__name__}"
                self.logger.warning("an http error occurred during the api request", extra={"extra": extra_msg})
                status_code = ex.args[1]
                if status_code >= 500:
                    retry_number += 1
                    time.sleep(self.configurations.sleep_time_between_retries)
                else:
                    break

            except Exception as ex:
                extra_msg = f"exception is {str(ex)}, exception_type is {type(ex).__name__}"
                self.logger.error("an unexpected error occurred while trying to get the number of repo commits",
                                  extra={"extra": extra_msg})
                break

        if retry_number == self.configurations.max_retries:
            self.logger.error("failed to execute the api request successfully after retries")

    def get_contributors_per_amount_of_commits(self, contributors: list) -> list:
        try:
            sorted_contributors = sorted(contributors, key=lambda x: x["contributions"], reverse=True)
            contributors_per_amount_of_commits = [x["login"] for x in sorted_contributors]
            return contributors_per_amount_of_commits
        except Exception as ex:
            extra_msg = f"exception is {str(ex)}, exception_type is {type(ex).__name__}"
            self.logger.error("an unexpected error occurred while trying to get contributors per amount of commits",
                              extra={"extra": extra_msg})

    def get_contributors_per_amount_of_pull_requests(self, pull_requests: list) -> list:
        try:
            contributors_list = []
            contributors = {}
            for pull_request in pull_requests:
                contributor = pull_request["user"]["login"]
                if contributor in contributors:
                    contributors[contributor] += 1
                else:
                    contributors[contributor] = 1

            for contributor, pull_requests in contributors.items():
                contributors_list.append({"contributor": contributor, "pull_requests": pull_requests})
            contributors_per_amount_of_pull_requests_mapping = sorted(contributors_list,
                                                                      key=lambda x: x["pull_requests"],
                                                                      reverse=True)
            contributors_per_amount_of_pull_requests = [contributor["contributor"] for contributor in
                                                        contributors_per_amount_of_pull_requests_mapping]
            return contributors_per_amount_of_pull_requests

        except Exception as ex:
            extra_msg = f"exception is {str(ex)}, exception_type is {type(ex).__name__}"
            self.logger.error("an unexpected error occurred while trying to get contributors per amount of pull requests",
                              extra={"extra": extra_msg})
