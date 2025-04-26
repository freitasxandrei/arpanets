from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Questionnaire, Answer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

# Função para redirecionar para a página de login ou questionário
@login_required
def home_redirect_view(request):
    return redirect('login')  # Redireciona para o questionário se o usuário estiver logado

# Register view for creating a new user
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Fazer o login automaticamente após o registro
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                auth_login(request, user)
                return redirect('questionnaire')  # Redireciona para o questionário após o registro e login
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('questionnaire')  # Redireciona para o questionário após o login
        else:
            return HttpResponse("Credenciais inválidas.")
    return render(request, 'core/login.html')

# Dashboard view (just a placeholder for now)
@login_required
def dashboard_view(request):
    return render(request, 'core/dashboard.html')

# Logout view
@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')

# Questionnaire view
@login_required
def questionnaire(request):
    if request.method == 'POST':
        responses = {}
        # Verificar se todas as respostas foram preenchidas
        for i in range(1, 21):
            response = request.POST.get(f"question_{i}")
            if not response:  # Se a resposta estiver vazia, interrompe e exibe erro
                return HttpResponse("Por favor, preencha todas as perguntas antes de enviar.")
            responses[f"question_{i}"] = response  # Armazenar 'Sim' ou 'Não' diretamente
        
        # Calculando a pontuação total
        total_score = sum([1 for response in responses.values() if response == 'Sim'])

        # Classificando o nível de sofrimento de acordo com a pontuação
        if total_score == 0:
            suffering_level = "Não foi identificado sofrimento mental de acordo com os parâmetros do SRQ-20."
        elif total_score <= 7:
            suffering_level = "Sofrimento mental leve."
        elif total_score <= 14:
            suffering_level = "Sofrimento mental moderado."
        else:
            suffering_level = "Sofrimento mental grave."

        # Criando o questionário no banco de dados
        questionnaire = Questionnaire.objects.create(
            user=request.user,
            total_score=total_score,
            suffering_level=suffering_level,
            response_date=timezone.now()
        )

        # Salvando as respostas no banco
        for i in range(1, 21):
            Answer.objects.create(
                questionnaire=questionnaire,
                question_number=i,
                answer=responses[f"question_{i}"]  # Salva 'Sim' ou 'Não'
            )
        
        # Redireciona para o resultado do questionário
        return redirect('questionnaire_result', pk=questionnaire.pk)

    return render(request, 'core/questionnaire.html')

# Questionnaire result view
@login_required
def questionnaire_result(request, pk):
    questionnaire = Questionnaire.objects.get(pk=pk)
    answers = questionnaire.answer_set.all()
    return render(request, 'core/questionnaire_result.html', {'questionnaire': questionnaire, 'answers': answers})