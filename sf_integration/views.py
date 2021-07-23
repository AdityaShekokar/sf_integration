from rest_framework import status
from rest_framework.views import APIView

from sf_integration.serializer import BaseResponseSerializer
from sf_integration.services.sf_account_service import AccountsListService, UserListService, ContactListService


class AccountsListView(APIView):
    @staticmethod
    def get(_):
        try:
            return AccountsListService.execute({})
        except Exception as e:
            return BaseResponseSerializer.error_response(
                e,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="SomethingWentWrong"
            )


class UserListView(APIView):
    @staticmethod
    def get(_):
        try:
            return UserListService.execute({})
        except Exception as e:
            return BaseResponseSerializer.error_response(
                e,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="SomethingWentWrong"
            )


class ContactListView(APIView):
    @staticmethod
    def get(_):
        try:
            return ContactListService.execute({})
        except Exception as e:
            return BaseResponseSerializer.error_response(
                e,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="SomethingWentWrong"
            )

