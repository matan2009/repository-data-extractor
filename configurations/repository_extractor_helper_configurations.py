class RepositoryExtractorHelperConfigurations:

    def __init__(self, max_retries: int, sleep_time_between_retries: int):
        self.max_retries = max_retries
        self.sleep_time_between_retries = sleep_time_between_retries
