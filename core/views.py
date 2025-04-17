from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'core/login.html', {'error': 'Usuário ou senha inválidos'})
    return render(request, 'core/login.html')

def dashboard_view(request):
    return render(request, 'core/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home_redirect_view(request):
    return redirect('login')

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SRQ20Response
from .serializers import SRQ20ResponseSerializer

@api_view(['GET', 'POST'])
def srq20_response_list(request):
    """
    Listar todas as respostas do SRQ-20 ou criar uma nova resposta.
    """
    if request.method == 'GET':
        responses = SRQ20Response.objects.all()
        serializer = SRQ20ResponseSerializer(responses, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SRQ20ResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
