import argparse

from monitoring.logger import create_logger
from service.repository_extractor_helper import RepositoryExtractorHelper


def main():
    latest_releases = repository_extractor_helper.get_repo_latest_releases()
    print(latest_releases)
    num_of_forks = repository_extractor_helper.get_number_of_repo_forks()
    print(num_of_forks)
    num_of_stars = repository_extractor_helper.get_number_of_repo_stars()
    print(num_of_stars)
    contributors = repository_extractor_helper.get_repo_contributors()
    num_of_contributors = len(contributors)
    print(num_of_contributors)
    pull_requests = repository_extractor_helper.get_repo_pull_requests()
    num_of_pull_requests = len(pull_requests)
    print(num_of_pull_requests)
    num_of_commits = repository_extractor_helper.get_number_of_repo_commits()
    print(num_of_commits)
    contributors_per_amount_of_commits = repository_extractor_helper.get_contributors_per_amount_of_commits(contributors)
    print(contributors_per_amount_of_commits)
    contributors_per_amount_of_pull_requests = repository_extractor_helper.get_contributors_per_amount_of_pull_requests(pull_requests)
    print(contributors_per_amount_of_pull_requests)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Accept a GitHub token and forked repo')
    parser.add_argument('token', type=str, help='a GitHub token')
    parser.add_argument('repo_name', type=str, help='forked repo')
    args = parser.parse_args()
    token = args.token
    repo_name = args.repo_name
    base_api_endpoint = f'https://api.github.com/repos/{repo_name}' #todo: move to configurations
    headers = {'Authorization': f'token {token}'}
    logger = create_logger()
    repository_extractor_helper = RepositoryExtractorHelper(logger, base_api_endpoint, headers)
    main()
