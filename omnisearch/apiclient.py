import json
from urllib.parse import urlencode
import requests
from omnisearch import exceptions


def clean_params(params: dict):
    return {k: v for k, v in params.items() if v}


def merge_url(url: str, params: dict):
    if params and len(params) > 0:
        return url + "?" + urlencode(clean_params(params))
    return url


class ApiClient:
    def __init__(self, logger, api_key, api_host, api_version, **kwargs):
        """
        :param logger: Logger
        :param base_uri: The base URI to the API
        :param version: API version
        """
        self.logger = logger
        self.api_host = api_host
        self.api_version = api_version
        self.api_key = api_key

        for k, v in kwargs.items():
            setattr(self, k, v)

        self.session = requests.Session()

    @property
    def api_host(self):
        return self._api_host

    @api_host.setter
    def api_host(self, value):
        """The default api_host"""
        if value and value.endswith("/"):
            value = value[:-1]
        self._api_host = value

    @staticmethod
    def headers(self):
        return {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

    def request(self, method, url, data=None, params=None):
        # Add the api key to params
        params["key"] = self.api_key

        if type(data) == dict:
            data = json.dumps(data)

        full_url = merge_url(f"{self.api_host}/{self.api_version}{url}", params)
        self.logger.info(full_url)

        result = self.session.request(
            method=method, url=full_url, data=data, headers=self.headers
        )
        if result.status_code == 200:
            return json.loads(result.text)

        raise exceptions.OmniSearchError
