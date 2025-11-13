from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_503_SERVICE_UNAVAILABLE, HTTP_200_OK


@api_view(["GET"])
def healthcheck(request):
    """
    Health check endpoint to verify service and database connectivity.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return Response(
            {"status": "healthy", "database": "connected"}, status=HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"status": "unhealthy", "database": "disconnected", "error": str(e)},
            status=HTTP_503_SERVICE_UNAVAILABLE,
        )
