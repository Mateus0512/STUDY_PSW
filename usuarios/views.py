from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages,auth

# Create your views here.
def cadastro(request):
    if request.method == 'GET':
        return render(request,'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(request,constants.ERROR,'As senhas estão diferentes')
            return redirect(reverse('cadastro'))
        
        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(request,constants.ERROR,'Usuário já existe!')
            return redirect(reverse('cadastro'))
        
        try:
            User.objects.create_user(username=username,password=senha)
            return redirect(reverse('login'))
        except:
            messages.add_message(request,constants.ERROR,'Erro interno do Servidor!')
            return redirect(reverse('cadastro'))
        
def logar(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = auth.authenticate(request,username=username,password=senha)

        if user:
            auth.login(request,user)
            return redirect(reverse('novo_flashcard'))
        else:
            messages.add_message(request,constants.ERROR,'Username ou senha Invalida')
            return redirect(reverse('logar'))
        
def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))