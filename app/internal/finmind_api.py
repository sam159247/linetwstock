from typing import Optional

import requests
from loguru import logger
from pydantic import ValidationError
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.core.config import settings
from app.exceptions import RequestMethodNotSupportError
from app.internal.models import stock_price


class FindMindAPI:

    base_url: str = settings.FINMIND_BASE_URL
    token: str = settings.FINMIND_TOKEN

    @classmethod
    def stock_price(cls, stock_id: str, start_date: str, end_date: Optional[str] = None) -> list[stock_price.Datum]:
        """Get stock price information.

        Find stcok basic information with a ticker symbol
        which between start date and end date.

        Args:
            stock_id (str)
            start_date (str)
            end_date (str)
            Refer to https://finmind.github.io/tutor/TaiwanMarket/Technical/#taiwanstockprice

        Returns:
            message (dict): Output Finmind message's raw data.
        """

        parameter = {
            "dataset": "TaiwanStockPrice",
            "data_id": stock_id,
            "start_date": start_date,
            "end_date": end_date,
            "token": cls.token,
        }
        result = cls._request_api(method="GET", url=cls.base_url, payload=parameter)
        try:
            message = stock_price.Message(**result.json())
            logger.info(message.json())
        except ValidationError as e:
            logger.exception(e)
            raise e

        return message.data

    @classmethod
    def _request_api(cls, method: str, url: str, payload: dict) -> requests.Response:
        """FinMind API Request base method.

        Args:
            method (str): request methods GET or POST
            url (str): FinMind API url
            payload (dict): request payload

        Raises:
            RequestMethodNotSupportError: HTTP methods not allowed.
            e: All exceptions that Requests explicitly raised inherit.

        Returns:
            requests.Response: The Response object, which contains a server’s response to an HTTP request.
        """

        retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        try:
            if method == "GET":
                resp = http.get(url, params=payload, timeout=(3, 10))
            elif method == "POST":
                resp = http.post(url, data=payload, timeout=(3, 10))
            else:
                raise RequestMethodNotSupportError(method)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.exception(f"HttpError: {e.response.text}")
            raise e
        except requests.exceptions.ConnectionError as e:
            logger.exception(f"ConnectionError: {e}")
            raise e
        except requests.exceptions.Timeout as e:
            logger.exception(f"TimeoutError: {e}")
            raise e
        except requests.exceptions.RequestException as e:
            logger.exception(f"RequestException: {e}")
            raise e

        return resp
