import time
import json

import requests

repo_name = "CTFd/CTFd"
base_api_endpoint = f'https://api.github.com/repos/{repo_name}'
# headers = {'Authorization': f'token {token}'}
max_retries = 5
sleep_time = 3

# todo: moving this constants to configuration file


def get_repo_latest_releases():
    # latest_releases_info = {}
    latest_releases_names = []
    releases_endpoint = "/releases"
    api_endpoint = base_api_endpoint + releases_endpoint
    retry_number = 0
    while retry_number < max_retries:
        try:
            response = requests.get(api_endpoint, headers=headers)
            if not response.status_code == 200:
                raise Exception()
            latest_releases = json.loads(response.content)[:3]
            for release in latest_releases:
                latest_releases_names.append(release["name"])
            return latest_releases_names

        except Exception as ex:
            print(ex)
            # todo: adding logger
            retry_number += 1
            time.sleep(sleep_time)


def get_number_of_repo_forks():
    retry_number = 0
    while retry_number < max_retries:
        try:
            response = requests.get(base_api_endpoint, headers=headers)
            if not response.status_code == 200:
                raise Exception()
            return response.json()['forks_count']

        except Exception as ex:
            print(ex)
            # todo: adding logger
            retry_number += 1
            time.sleep(sleep_time)


def main():
    latest_releases = get_repo_latest_releases()
    print(latest_releases)
    num_of_forks = get_number_of_repo_forks()
    print(num_of_forks)


if __name__ == '__main__':
    main()
