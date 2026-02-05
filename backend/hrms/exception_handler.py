from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.db import IntegrityError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        return response
    
    if isinstance(exc, ValidationError):
        return Response(
            {'error': str(exc)},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if isinstance(exc, IntegrityError):
        error_msg = str(exc)
        if 'unique constraint' in error_msg.lower() or 'duplicate' in error_msg.lower():
            return Response(
                {'error': 'A record with this information already exists.'},
                status=status.HTTP_409_CONFLICT
            )
        return Response(
            {'error': 'Database integrity error occurred.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response(
        {'error': 'An unexpected error occurred.'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )