import requests
from .serializers import UserSerializer
from django.contrib.auth.models import Group, User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['GET'])
def getUser(request, uid):
    user = User.objects.filter(id=uid)
    serializer = UserSerializer(user, many=True)
    return Response({'user': serializer.data})


@api_view(['POST'])
def getUserFromToken(request):

    token = request.data['token']
    if(token == None):
        token = ""

    response = requests.get('http://localhost:8000/auth/users/me/',
                            headers={"Authorization": "Token "+token})

    if response.status_code != 200:
        print("gone")
        return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)

    user = response.json()
    user = User.objects.get(id=user['id'])
    serializer = UserSerializer(user, many=False)
    return Response({'user': serializer.data, "token": token})


@api_view(['GET', 'POST'])
def login(request):
    body = request.data
    response = requests.post(
        'http://localhost:8000/auth/token/login', data=body)

    if response.status_code != 200:
        print("if block")
        return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)

    token = response.json()['auth_token']
    res = requests.post(
        'http://localhost:8000/auth/getUserFromToken', data={"token": token})
    return Response(res.json())
    # user = requests.get('http://localhost:8000/auth/users/me/',
    #                     headers={"Authorization": "Token "+token})
    # user = user.json()
    # user = User.objects.get(id=user['id'])
    # serializer = UserSerializer(user, many=False)
    # return Response({'user': serializer.data, "token": token})
