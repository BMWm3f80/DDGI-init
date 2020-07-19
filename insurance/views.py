from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from insurance.serializers import *
from rest_framework import viewsets


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def test_view(request):
    response = {}
    response['success'] = True
    response['authenticated_user'] = request.user.username
    return Response(response)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class PositionsViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated, ]
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    # def create(self, request, *args, **kwargs):
    #     print("Create")
    #     return Response(self.request.data)
    #
    # def update(self, request, *args, **kwargs):
    #     print("update")
    #     return Response(self.request.data)

    # def destroy(self, request, *args, **kwargs):
    #     print("DELETE")
    #     return Response(self.request.data)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
