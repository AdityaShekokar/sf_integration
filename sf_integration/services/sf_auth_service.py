import logging
import time

from django.conf import settings

import requests
from requests.adapters import HTTPAdapter
from rest_framework import status
from urllib3 import Retry

from sf_integration.constants import auth_constant
from sf_integration.settings import (
    SF_BASE_URL,
    SF_CLIENT_ID,
    SF_CLIENT_SECRET,
    SF_PASSWORD,
    SF_USERNAME,
    TLS_VERIFY,
)

logger = logging.getLogger(__name__)


class SalesForceImpl:
    token = None
    _request_session = None
    _request_timeout = None
    _request_retrieves = None
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if SalesForceImpl.__instance is None:
            SalesForceImpl()
        return SalesForceImpl.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if SalesForceImpl.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SalesForceImpl.__instance = self

    @classmethod
    def clear(cls):
        cls.token = None
        cls._request_session = None
        cls._request_timeout = None
        cls._request_retrieves = None
        cls.__instance = None

    @classmethod
    def get_authenticate(cls, refreshed=""):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "username": SF_USERNAME,
            "password": SF_PASSWORD,
            "grant_type": auth_constant["GrantType"],
            "client_id": SF_CLIENT_ID,
            "client_secret": SF_CLIENT_SECRET,
        }
        response = cls.make_request(
            SF_BASE_URL + "services/oauth2/token",
            auth_constant["MethodPOST"],
            headers,
            data,
        )
        if response.status_code == status.HTTP_200_OK:
            cls.token = response.json().get("access_token")
            logger.info("Authentication {}success".format(refreshed))
        else:
            logger.error(str(response.json()))
            raise Exception(
                "The authentication returned status code: {}".format(
                    response.status_code
                )
            )

    @classmethod
    def execute_query(cls, url, method=auth_constant["MethodGET"], data=None):
        if cls.token is None:
            cls.get_authenticate()

        response = cls.make_request(url, method, cls.__make_headers(), data)

        if cls.__refresh_token(response.status_code, response):
            response = cls.make_request(url, method, cls.__make_headers(), data)

        return response

    @classmethod
    def __get_request_session(cls):
        if cls._request_session is not None:
            session = cls._request_session
        else:
            cls._request_timeout = settings.REQUEST_CONFIG.get("TIMEOUT")
            session = requests.Session()
            retry = Retry(
                total=settings.REQUEST_CONFIG.get("NUM_RETRIES"),
                read=settings.REQUEST_CONFIG.get("NUM_RETRIES"),
                connect=settings.REQUEST_CONFIG.get("NUM_RETRIES"),
                backoff_factor=settings.REQUEST_CONFIG.get("BACKOFF_FACTOR"),
                status_forcelist=settings.REQUEST_CONFIG.get("STATUS_FORCE_RETRY"),
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("https://", adapter)
            cls._request_session = session
        return session

    @classmethod
    def __refresh_token(cls, status_code, response):
        body = None
        try:
            body = response.json()
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            logger.warning("Decoding JSON has failed")

        if (
            status_code is not None
            and status_code == requests.codes.unauthorized
            and len(body) > 0
            and body[0].get("errorCode") == "INVALID_SESSION_ID"
        ):
            cls.get_authenticate("refreshed ")
            return True
        return False

    @classmethod
    def __make_headers(cls, token=None):
        if token is None:
            token = cls.token
        return {
            "Content-type": "application/json; odata=verbose",
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        }

    @classmethod
    def make_request(
        cls, url, method=auth_constant["MethodGET"], headers=None, data=None
    ):
        cls.__get_request_session().verify = TLS_VERIFY
        if data is None:
            data = {}
        if headers is None:  # pragma: no cover
            headers = {}
        timeout = settings.REQUEST_CONFIG.get("TIMEOUT")
        attempts = settings.REQUEST_CONFIG.get("NUM_RETRIES")
        t0 = time.time()
        try:
            response = cls.__get_request_session().request(
                method,
                url,
                data=data,
                headers=headers,
                timeout=timeout,
            )
        except Exception as e:
            logger.error(e)
            msg_error = "Failed the SF request did not respond correctly after {} attempts".format(
                attempts
            )
            raise Exception(msg_error)
        else:
            logger.info(
                "The SF request returned status code: {}".format(response.status_code)
            )
        finally:
            t1 = time.time()
            logger.debug("The SF request took {} seconds".format(t1 - t0))
        return response
