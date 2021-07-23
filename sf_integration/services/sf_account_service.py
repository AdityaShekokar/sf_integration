from http import HTTPStatus

from rest_framework import status
from rest_framework.response import Response
from service_objects.services import Service

from db.models import Contacts, Users, Accounts
from sf_integration.constants import URI_API_SALESFORCE_Q
from sf_integration.serializer import BaseResponseSerializer, SFAccount
from sf_integration.services.sf_auth_service import SalesForceImpl
from sf_integration.settings import SF_BASE_URL

SF_INSTANCE = SalesForceImpl.get_instance()


def check_record_already_exist(model_name, serial_data):
    for data in serial_data:
        if model_name == "Contacts":
            record = Contacts.objects.filter(sf_contact_id=data.get("Id"))
        if model_name == "Accounts":
            record = Accounts.objects.filter(sf_account_id=data.get("Id"))
        if model_name == "Users":
            record = Users.objects.filter(sf_user_id=data.get("Id"))
    if record:
        return Response("already exist", status=HTTPStatus.OK)
    return Response("no record found", status=HTTPStatus.NOT_FOUND)


def save_obejcts_in_database(model_name, serial_data):
    for data in serial_data:
        sf_id = data.get("Id")
        name = data.get("Name")
        phone = data.get("Phone")
        if model_name == "Contacts":
            Contacts.objects.create(sf_contact_id=sf_id, name=name, phone=phone)
        if model_name == "Accounts":
            Accounts.objects.create(sf_account_id=sf_id, name=name, phone=phone)
        if model_name == "Users":
            Users.objects.create(sf_user_id=sf_id, name=name, phone=phone)


class AccountsListService(Service):

    def process(self):
        """
        :return: status_code with response in json-form.
        """
        url = (
            f"{SF_BASE_URL}{URI_API_SALESFORCE_Q}/?q=SELECT Id, Name, Phone, BillingAddress FROM Account"
        )
        try:
            response = SF_INSTANCE.execute_query(url)
            if response.status_code == status.HTTP_200_OK:
                serializer = SFAccount(
                    data=response.json().get("records"), many=True
                )
                if serializer.is_valid():
                    response = check_record_already_exist("Accounts", serializer.data)
                    if response.status_code != 200:
                        save_obejcts_in_database("Accounts", serializer.data)
                    return BaseResponseSerializer.success_response(
                        serializer.data,
                        response.status_code,
                        message=f"Successfully fetched {len(serializer.data)} accounts",
                    )
                else:
                    return BaseResponseSerializer.error_response(
                        serializer.errors,
                        response.status_code,
                        message=f"Could not retrieve the accounts",
                    )
            return BaseResponseSerializer.error_response(
                [response.text],
                response.status_code,
                message=f"Could not retrieve the accounts",
            )
        except Exception as e:
            return BaseResponseSerializer.error_response(
                e,
                500,
                message=f"Could not retrieve the accounts",
            )


class UserListService(Service):

    def process(self):
        """
        :return: status_code with response in json-form.
        """
        url = (
            f"{SF_BASE_URL}{URI_API_SALESFORCE_Q}/?q=SELECT Id, Name, Phone FROM User"
        )
        try:
            response = SF_INSTANCE.execute_query(url)
            if response.status_code == status.HTTP_200_OK:
                serializer = SFAccount(
                    data=response.json().get("records"), many=True
                )
                if serializer.is_valid():
                    response = check_record_already_exist("Users", serializer.data)
                    if response.status_code != 200:
                        save_obejcts_in_database("Users", serializer.data)
                    return BaseResponseSerializer.success_response(
                        serializer.data,
                        response.status_code,
                        message=f"Successfully fetched {len(serializer.data)} users",
                    )
                else:
                    return BaseResponseSerializer.error_response(
                        serializer.errors,
                        response.status_code,
                        message=f"Could not retrieve the users",
                    )
            return BaseResponseSerializer.error_response(
                [response.text],
                response.status_code,
                message=f"Could not retrieve the users",
            )
        except Exception as e:
            return BaseResponseSerializer.error_response(
                e,
                500,
                message=f"Could not retrieve the users",
            )


class ContactListService(Service):

    def process(self):
        """
        :return: status_code with response in json-form.
        """
        url = (
            f"{SF_BASE_URL}{URI_API_SALESFORCE_Q}/?q=SELECT Id, Name, Phone FROM Contact"
        )
        try:
            response = SF_INSTANCE.execute_query(url)
            if response.status_code == status.HTTP_200_OK:
                serializer = SFAccount(
                    data=response.json().get("records"), many=True
                )
                if serializer.is_valid():
                    response = check_record_already_exist("Contacts", serializer.data)
                    if response.status_code != 200:
                        save_obejcts_in_database("Contacts", serializer.data)
                    return BaseResponseSerializer.success_response(
                        serializer.data,
                        response.status_code,
                        message=f"Successfully fetched {len(serializer.data)} contacts",
                    )
                else:
                    return BaseResponseSerializer.error_response(
                        serializer.errors,
                        response.status_code,
                        message=f"Could not retrieve the contacts",
                    )
            return BaseResponseSerializer.error_response(
                [response.text],
                response.status_code,
                message=f"Could not retrieve the contacts",
            )
        except Exception as e:
            return BaseResponseSerializer.error_response(
                e,
                500,
                message=f"Could not retrieve the contacts",
            )
