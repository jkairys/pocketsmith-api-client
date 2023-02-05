from enum import Enum
from typing import Any, Dict

from requests import request
from pydantic import BaseModel, SecretStr
from loguru import logger


class HttpMethod(Enum):
    """
    HTTP Methods for API client
    """

    GET = "get"
    POST = "post"


class Api(BaseModel):
    """
    Pocketsmith REST API client
    """

    developer_key: SecretStr
    base_url = "https://api.pocketsmith.com/v2"
    timeout = 5

    def call(
        self,
        method: HttpMethod,
        route: str,
        params: Dict[str, str] = None,
        data: Any = None,
        headers: Dict[str, str] = None,
    ) -> Any:
        """
        Wrapper method for requests call method
        """
        _headers = {
            **(headers if headers else {}),
            "X-Developer-Key": self.developer_key.get_secret_value(),
            "Accept": "application/json",
        }

        url = f"{self.base_url}{route}"
        kwargs = {}
        if data:
            kwargs["json"] = data
        if params:
            kwargs["params"] = params

        logger.debug(f"Calling URL {url} with headers={_headers}, kwargs={kwargs}")
        result = request(
            method=method.value,
            url=url,
            timeout=self.timeout,
            headers=_headers,
            **kwargs,
        )
        if result.status_code >= 400:
            raise RuntimeError(result.content)
        return result.json()

    def get(
        self,
        route: str,
        params: Dict[str, str] = None,
        data: Any = None,
        headers: Dict[str, str] = None,
    ) -> Any:
        """
        Wrapper for HTTP GET calls
        """
        return self.call(
            HttpMethod.GET, route=route, params=params, data=data, headers=headers
        )

    def post(
        self, route: str, params: Dict[str, str], data: Any, headers: Dict[str, str]
    ) -> Any:
        """
        Wrapper for HTTP POST calls
        """
        return self.call(
            HttpMethod.POST, route=route, params=params, data=data, headers=headers
        )
