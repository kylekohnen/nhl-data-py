from nhl_data_py.nhl_api.nhl_api import NhlApi


class TestNhlApi:
    """
    Tests the NhlApi class from the `nhl_data_py.nhl_api.nhl_api` module.
    """

    # We should make tests much more reliable and
    # not dependent at all on the actual API (mock API?)
    def test_get_non_existent_endpoint(self):
        nhl = NhlApi()
        response = nhl.get("ooga_booga_ya_doesnt_exist")
        assert response.status_code == 404
