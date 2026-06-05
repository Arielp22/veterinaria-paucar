from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ErrorDetail, NotAuthenticated, PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def _normalize_detail(detail):
    if isinstance(detail, dict):
        return {key: _normalize_detail(value) for key, value in detail.items()}
    if isinstance(detail, list):
        return [_normalize_detail(value) for value in detail]
    if isinstance(detail, ErrorDetail):
        return str(detail)
    return detail


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        payload = {
            'status_code': response.status_code,
            'error': response.status_text,
            'detail': _normalize_detail(response.data),
        }
        return Response(payload, status=response.status_code)

    if isinstance(exc, Http404):
        return Response(
            {'status_code': status.HTTP_404_NOT_FOUND, 'error': 'Not Found', 'detail': 'No se encontró el recurso solicitado.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if isinstance(exc, (ValidationError, PermissionDenied, NotAuthenticated)):
        return Response(
            {'status_code': status.HTTP_400_BAD_REQUEST, 'error': 'Bad Request', 'detail': 'Solicitud inválida.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'error': 'Internal Server Error', 'detail': 'Ocurrió un error inesperado.'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )