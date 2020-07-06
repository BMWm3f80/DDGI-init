from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def test_view(request):
    response = {}
    response['success'] = True
    response['authenticated_user'] = request.user.username
    return Response(response)