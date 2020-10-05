from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from insurance.serializers import *
from rest_framework import viewsets
import json
import datetime
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
    permission_classes = [IsAuthenticated, ]
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
    permission_classes = [IsAuthenticated, ]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
       # print(json.loads(self.request.query_params.get('filter_param'))["status"])
        queryset = Profile.objects.all()
        return queryset


class PermissionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class GridViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Dt_Option.objects.all()
    serializer_class = DtOptionSerializer

    def create(self, request, *args, **kwargs):
        if Dt_Option.objects.filter(codeName=request.data['gridCodeName']).exists():
            grid = Dt_Option.objects.get(codeName=request.data['gridCodeName'])
            serializer = DtOptionSerializer(grid, read_only=True)
            return Response(serializer.data)


class IndividualClientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = IndividualClient.objects.all()
    serializer_class = IndividualClientSerializer

    def create(self, request, *args, **kwargs):
        response = {}
        try:
            if self.request.data['action'] == 'create':
                params = self.request.data['params']
                IndividualClient.objects.create(
                    first_name=params['first_name'],
                    last_name=params['last_name'],
                    middle_name=params['middle_name'],
                    address=params['address'],
                    phone_number=params['phone_number'],
                    cr_by=self.request.user
                ).save()
            elif self.request.data['action'] == 'get':
                item_id = self.request.data['id']
                item = IndividualClient.objects.get(id=item_id)
                serializer = IndividualClientSerializer(item)
                response['success'] = True
                response['data'] = serializer.data
            elif self.request.data['action'] == 'update':
                params = self.request.data['params']
                IndividualClient.objects.filter(id=params['id']).update(
                    first_name=params['first_name'],
                    last_name=params['last_name'],
                    middle_name=params['middle_name'],
                    address=params['address'],
                    phone_number=params['phone_number'],
                    up_by=self.request.user,
                    up_on=datetime.datetime.now()
                )
            elif self.request.data['action'] == 'delete':
                item_id = self.request.data['id']
                IndividualClient.objects.filter(id=item_id).update(
                    is_exist=False
                )
        except Exception as e:
            response['success'] = False
            response['error_msg'] = str(e)
        return Response(response)


class RegisterPoliseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = RegisteredPolises.objects.filter(is_exist=True)
    serializer_class = RegisteredPoliseSerializer

    def create(self, request, *args, **kwargs):
        response = {}
        #req = json.loads(self.request.data)
        try:
            if str(self.request.data['action']) == 'create':
                params = json.loads(self.request.data['params'])
                RegisteredPolises.objects.create(
                    act_number=params['act_number'],
                    act_date=params['act_date'],
                    polis_number_from=params['polis_number_from'],
                    polis_number_to=params['polis_number_to'],
                    polis_quantity=params['polis_quantity'],
                    polis_status=params['polis_status'],
                    document=self.request.FILES['file'],
                    cr_by=self.request.user
                ).save()
                response['success'] = True
            elif self.request.data['action'] == 'get':
                item_id = self.request.data['id']
                item = RegisteredPolises.objects.get(id=item_id)
                serializer = RegisteredPoliseSerializer(item)
                response['data'] = serializer.data
            elif str(self.request.data['action']) == 'update':
                print(self.request.content_type)
                print(self.request.data)
                print(self.request.FILES)
                if self.request.FILES['file']:
                    print(self.request.data)
                    print(self.request.FILES)
        except Exception as e:
            response['success'] = False
            response['error_msg'] = str(e)
        return Response(response)


class CurrencyViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Currency.objects.filter(is_exist=True)
    serializer_class = CurrencySerializer

    def create(self, request, *args, **kwargs):
        response = {}
        try:
            if self.request.data['action'] == 'create':
                params = self.request.data['params']
                Currency.objects.create(
                    name=params['name'],
                    code=params['code']
                ).save()
                response['success'] = True
            elif self.request.data['action'] == 'get':
                item_id = self.request.data['id']
                item = Currency.objects.get(id=item_id)
                serializer = CurrencySerializer(item)
                response['success'] = True
                response['data'] = serializer.data
            elif self.request.data['action'] == 'update':
                params = self.request.data['params']
                Currency.objects.filter(id=params['id']).update(
                    name=params['name'],
                    code=params['code']
                )
                response['success'] = True
            elif self.request.data['delete']:
                params = self.request.data['params']
                Currency.objects.filter(id=params['id']).update(
                    is_exist=False
                )
                response['success'] = True
        except Exception as e:
            print(e)
            response['success'] = False
            response['error_msg'] = str(e)
        return  Response(response)


class GroupViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        response = {}
        try:
            if self.request.data['action'] == 'create':
                params = self.request.data['params']
                Group.objects.create(
                    name=params['name']
                ).save()
                response['success'] = True
            elif self.request.data['action'] == 'get':
                item_id = self.request.data['id']
                item = Group.objects.get(id=item_id)
                serializer = GroupSerializer(item)
                response['data'] = serializer.data
                response['success'] = True
            elif self.request.data['params'] == 'update':
                params = self.request.data['params']
                Group.objects.filter(id=params['id']).update(
                    name=params['name']
                )
                response['success'] = True
            elif self.request.data['action'] == 'delete':
                item_id = self.request.data['id']
                Group.objects.filter(id=item_id).update(
                    is_exist=False
                )
                response['success'] = True
        except Exception as e:
            response['success'] = False
            response['error_msg'] = str(e)
        return Response(response)


class KlassViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Klass.objects.filter(is_exist=True)
    serializer_class = KlassSerializer

    def create(self, request, *args, **kwargs):
        response = {}
        try:
            if self.request.data['action'] == 'create':
                params = self.request.data['params']
                Klass.objects.create(
                    name=params['name']
                ).save()
                response['success'] = True
            elif self.request.data['action'] == 'get':
                item_id = self.request.data['id']
                item = Klass.objects.get(id=item_id)
                serializer = KlassSerializer(item)
                response['data'] = serializer.data
                response['success'] = True
            elif self.request.data['action'] == 'update':
                params = self.request.data['params']
                Klass.objects.filter(id=params['id'], is_exist=True).update(
                    name=params['name']
                )
                response['success'] = True
            elif self.request.data['action'] == 'delete':
                item_id = self.request.data['id']
                Klass.objects.filter(id=item_id).update(
                    is_exist=False
                )
                response['success'] = True
        except Exception as e:
            response['success'] = False
            response['error_msg'] = str(e)
        return Response(response)


class BankViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Bank.objects.filter(is_exist=True)
    serializer_class = BankSerializer

    def create(self, request, *args, **kwargs):
        response = {}
        try:
            if self.request.data['action'] == 'create':
                params = self.request.data['params']
                Bank.objects.create(
                    name=params['name'],
                    mfo=params['mfo'],
                    inn=params['inn'],
                    address=params['address'],
                    phone_number=params['phone_number'],
                    checking_account=params['checking_account']

                ).save()
                response['success'] = True
            elif self.request.data['action'] == 'get':
                item_id = self.request.data['id']
                item = Bank.objects.get(id=item_id, is_exist=True)
                serializer = BankSerializer(item)
                response['data'] = serializer.data
                response['success'] = True
            elif self.request.data['action'] == 'update':
                params = self.request.data['params']
                Bank.objects.filter(id=params['id'], is_exist=True).update(
                    name=params['name'],
                    mfo=params['mfo'],
                    inn=params['inn'],
                    address=params['address'],
                    phone_number=params['phone_number'],
                    checking_account=params['checking_account']

                )
                response['success'] = True
            elif self.request.data['action'] == 'delete':
                item_id = self.request.data['id']
                Bank.objects.filter(id=item_id).update(
                    is_exist=False
                )
                response['success'] = True
        except Exception as e:
            response['success'] = False
            response['error_msg'] = str(e)
        return Response(response)


class BranchViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Branch.objects.filter(is_exist=True)
    serializer_class = BranchSerializer

    def create(self, request, *args, **kwargs):
        response = {}
        try:
            if self.request.data['action'] == 'create':
                params = self.request.data['params']
                director = User.objects.get(id=params['director'])
                Branch.objects.create(
                    name=params['name'],
                    director=director,
                    cr_by=self.request.user
                ).save()
                response['success'] = True
            elif self.request.data['action'] == 'get':
                item_id = self.request.data['id']
                item = Branch.objects.get(id=item_id)
                serializer = BranchSerializer(item)
                response['data'] = serializer.data
                response['success'] = True
            elif self.request.data['action'] == 'update':
                params = self.request.data['params']
                director = User.objects.get(id=params['director'])
                Branch.objects.filter(id=params['id']).update(
                    name=params['name'],
                    director=director,
                    up_by=self.request.user
                )
                response['success'] = True
            elif self.request.data['action'] == 'delete':
                item_id = self.request.data['id']
                Branch.objects.filter(id=item_id).update(
                    up_by=self.request.user,
                    is_exist=False
                )
        except Exception as e:
            response['success'] = False
            response['error_msg'] = str(e)
        return Response(response)


class LegalClientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = LegalClient.objects.filter(is_exist=True)
    serializer_class = LegalClientSerializer

    def create(self, request, *args, **kwargs):
        response = {}
        try:
            if self.request.data['action'] == 'create':
                params = self.request.data['params']
                LegalClient.objects.create(
                    name=params['name'],
                    address=params['address'],
                    phone_number=params['phone_number']
                ).save()
                response['success'] = True
            elif self.request.data['action'] == 'get':
                item_id = self.request.data['id']
                item = LegalClient.objects.get(id=item_id)
                response['data'] = LegalClientSerializer(item)
                response['success'] = True
            elif self.request.data['action'] == 'update':
                params = self.request.data['params']
                LegalClient.objects.filter(id=params['id']).update(
                    name=params['name'],
                    address=params['address'],
                    phone_number=params['phone_number'],
                    up_by=self.request.user
                )
                response['success'] = True
            elif self.request.data['action'] == 'delete':
                item_id = self.request.data['id']
                LegalClient.objects.filter(id=item_id).update(
                    up_by=self.request.user,
                    is_exist=False
                )
                response['success'] = True
        except Exception as e:
            response['success'] = False
            response['error_msg'] = str(e)
        return Response(response)



