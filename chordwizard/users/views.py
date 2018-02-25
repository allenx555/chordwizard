from django.shortcuts import render, redirect
from .forms import RegisterForm

import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import User, UserSerialiser
from chordwizard.helpers import InputErrorMessage, JSONResponse
from .admin import InviteCode


class UserShow(APIView):
    def get(self, request, format=None):
        serializer = UserSerialiser(request.user)
        return Response(serializer.data)


def registerview(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})


class Register(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return InputErrorMessage("Invalid JSON body")
        if "invitationcode" not in data:
            return InputErrorMessage("invitationcode not provide.")
        try:
            invitecode = InviteCode.objects.get(code=data["invitationcode"])
        except InviteCode.DoesNotExist:
            return InputErrorMessage(
                "invitationcode not exist.",
                status=status.HTTP_404_NOT_FOUND
                )
        if invitecode.used_by:
            return InputErrorMessage("invitationcode is used.")
        if "username" not in data:
            return InputErrorMessage("username not provide.")
        if User.objects.filter(username=data["username"]).exists():
            return InputErrorMessage("username is used.")
        if "email" not in data:
            return InputErrorMessage("email not provide.")
        if User.objects.filter(email=data["email"]).exists():
            return InputErrorMessage("email is used.")
        if "password" not in data:
            return InputErrorMessage("password not provide.")
        user = User.objects.create_user(username=data["username"],
                                        email=data["email"], password=data["password"])
        user.save()
        invitecode.used_by = user
        invitecode.save()
        return JSONResponse({
            "code": 200,
            "message": "OK",
        })


class ChangePassword(APIView):
    def post(self, request):

        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return InputErrorMessage(
                "Invalid JSON body",
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        if "old_password" not in data:
            return InputErrorMessage(
                "You must provide old password",
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        if not request.user.check_password(data["old_password"]):
            return InputErrorMessage(
                "old password not match",
                status=status.HTTP_403_FORBIDDEN
            )
        if "new_password" not in data:
            return InputErrorMessage(
                "You must provide new password",
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        request.user.set_password(data["new_password"])
        request.user.save()
        serializer = UserSerialiser(request.user)
        return Response(serializer.data)


def index(request):
    return render(request, 'index.html')

