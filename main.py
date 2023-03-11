import argparse

from monitoring.logger import create_logger
from service.repository_extractor_helper import RepositoryExtractorHelper


def main():
    latest_releases = repository_extractor_helper.get_repo_latest_releases()
    print(f"the latest 3 releases of {repo_name} repo are: {latest_releases}")
    num_of_forks = repository_extractor_helper.get_number_of_repo_forks()
    print(f"the number of forks that {repo_name} repo has is: {num_of_forks}")
    num_of_stars = repository_extractor_helper.get_number_of_repo_stars()
    print(f"the number of starts that {repo_name} repo has is: {num_of_stars}")
    contributors = repository_extractor_helper.get_repo_contributors()
    num_of_contributors = len(contributors)
    print(f"the number of contributors that {repo_name} repo has is: {num_of_contributors}")
    pull_requests = repository_extractor_helper.get_repo_pull_requests()
    num_of_pull_requests = len(pull_requests)
    print(f"the number of pull requests that {repo_name} repo has is: {num_of_pull_requests}")
    num_of_commits = repository_extractor_helper.get_number_of_repo_commits()
    print(f"the number of commits that {repo_name} repo has is: {num_of_commits}")
    contributors_per_amount_of_commits = repository_extractor_helper.get_contributors_per_amount_of_commits(contributors)
    print(f"the contributors per amount of commits that {repo_name} repo has is: {contributors_per_amount_of_commits}")
    contributors_per_amount_of_pull_requests = repository_extractor_helper.get_contributors_per_amount_of_pull_requests(pull_requests)
    print(f"the contributors per amount of pull requests that {repo_name} repo has is: {contributors_per_amount_of_pull_requests}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Accept a GitHub token and forked repo')
    parser.add_argument('token', type=str, help='a GitHub token')
    parser.add_argument('repo_name', type=str, help='forked repo')
    args = parser.parse_args()
    token = args.token
    repo_name = args.repo_name
    base_api_endpoint = f'https://api.github.com/repos/{repo_name}'
    headers = {'Authorization': f'token {token}'}
    logger = create_logger()
    repository_extractor_helper = RepositoryExtractorHelper(logger, base_api_endpoint, headers)
    main()
