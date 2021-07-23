from django.http import JsonResponse
from rest_framework import serializers

from db.models import Accounts, Users, Contacts


class BaseResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    message = serializers.CharField()
    code = serializers.IntegerField()


class ErrorListField(serializers.ListField):
    error = serializers.DictField()


class DataDictResponseSerializer(BaseResponseSerializer):
    data = serializers.DictField(required=False)


class DataListResponseSerializer(BaseResponseSerializer):
    data = serializers.ListField(child=serializers.DictField(), required=False)


class ErrorResponseSerializer(BaseResponseSerializer):
    success = serializers.BooleanField(default=False)
    errors = ErrorListField(required=True)


class BaseResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    message = serializers.CharField()
    code = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass  # BTD

    def create(self, validated_data):
        pass  # BTD

    @staticmethod
    def success_response(result, status, message=None):
        if message is None:
            message = "SuccessfullyCompleted"

        if isinstance(result, list):
            return JsonResponse(
                DataListResponseSerializer(
                    {
                        "success": True,
                        "data": result.data
                        if isinstance(result, serializers.ModelSerializer)
                        else result,
                        "code": status,
                        "message": "SuccessfullyCreated"
                        if status == 201
                        else message,
                    }
                ).data,
                safe=False,
                status=status,
            )

        return JsonResponse(
            DataDictResponseSerializer(
                {
                    "success": True,
                    "data": result.data
                    if isinstance(result, serializers.ModelSerializer)
                    else result,
                    "code": status,
                    "message": "SuccessfullyCreated"
                    if status == 201
                    else message,
                }
            ).data,
            safe=False,
            status=status,
        )

    @staticmethod
    def error_response(error, status, message):
        if isinstance(error, Exception):
            return JsonResponse(
                ErrorResponseSerializer(
                    {
                        "success": False,
                        "code": status,
                        "message": message,
                        "errors": [str(error)],
                        "data": {},
                    }
                ).data,
                safe=False,
                status=status,
            )
        if isinstance(error, list):
            return JsonResponse(
                ErrorResponseSerializer(
                    {
                        "message": message,
                        "code": status,
                        "errors": error,
                    }
                ).data,
                safe=False,
                status=status,
            )
        return JsonResponse(
            ErrorResponseSerializer(
                {
                    "message": message,
                    "code": status,
                    "errors": [error],
                }
            ).data,
            safe=False,
            status=status,
        )


class SFAccount(serializers.Serializer):
    """
    This serializer class is used to validate the request params of the "salesforce account".
    """

    Id = serializers.CharField(required=True, min_length=18)
    Name = serializers.CharField(required=False, allow_null=True)
    Phone = serializers.CharField(required=False, allow_null=True)
