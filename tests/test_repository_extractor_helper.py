from unittest import TestCase, mock

from service.repository_extractor_helper import RepositoryExtractorHelper


class TestCyberScansHelper(TestCase):

    @mock.patch("service.repository_extractor_helper.get_configurations")
    def setUp(self, mocked_config) -> None:
        mocked_config.return_value = {"repository_extractor_helper": {"max_retries": 3, "sleep_time_between_retries": 5}}
        self.helper = RepositoryExtractorHelper(logger=mock.Mock(), base_api_endpoint="https://base.api.endpoint",
                                                         headers={"Authorization": "token"})

    @mock.patch('requests.get')
    def test_get_repo_latest_releases_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b'[{"name": "1.1.1"}, {"name": "2.2.2"}, {"name": "3.3.3"}]'
        res = self.helper.get_repo_latest_releases()
        self.assertEqual(type(res), list)
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0], "1.1.1")
        self.assertEqual(res[1], "2.2.2")
        self.assertEqual(res[2], "3.3.3")

    @mock.patch('requests.get')
    def test_get_repo_latest_releases_failed_with_not_found(self, mock_get):
        mock_get.return_value.status_code = 404
        mock_get.return_value.content = b''
        res = self.helper.get_repo_latest_releases()
        self.assertIsNone(res)

    @mock.patch('requests.get')
    def test_get_repo_latest_releases_success_after_retry(self, mock_get):
        mock_get.side_effect = [mock.Mock(status_code=500, content=b''), mock.Mock(status_code=200,
                                                                                   content=b'[{"name": "1.1.1"}, '
                                                                                           b'{"name": "2.2.2"}, '
                                                                                           b'{"name": "3.3.3"}]')]
        res = self.helper.get_repo_latest_releases()
        self.assertEqual(type(res), list)
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0], "1.1.1")
        self.assertEqual(res[1], "2.2.2")
        self.assertEqual(res[2], "3.3.3")

    @mock.patch('requests.get')
    def test_get_number_of_repo_forks_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"forks_count": 3}
        res = self.helper.get_number_of_repo_forks()
        self.assertEqual(type(res), int)
        self.assertEqual(res, 3)

    @mock.patch('requests.get')
    def test_get_number_of_repo_forks_failed_with_not_found(self, mock_get):
        mock_get.return_value.status_code = 404
        res = self.helper.get_number_of_repo_forks()
        self.assertIsNone(res)

    @mock.patch('requests.get')
    def test_get_repo_contributors_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"login": "name", "node_id": "id", "url": "url"}]
        res = self.helper.get_repo_contributors()
        self.assertEqual(type(res), list)
        self.assertEqual(res, [{"login": "name", "node_id": "id", "url": "url"}])