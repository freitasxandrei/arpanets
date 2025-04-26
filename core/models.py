from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError

# Modelo customizado de usuário
class User(AbstractUser):
    gender = models.CharField(max_length=10, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)

# Modelo para armazenar as respostas ao questionário
class SRQ20Response(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="srq_responses")
    responses = models.JSONField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Respostas de {self.user.username} em {self.submitted_at.strftime('%Y-%m-%d')}"

# Modelo para armazenar o questionário respondido
class Questionnaire(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Usando AUTH_USER_MODEL
    response_date = models.DateTimeField(auto_now_add=True)
    total_score = models.IntegerField()

    # Aumentei o max_length para 50 e adicionei validação customizada
    suffering_level = models.CharField(max_length=50)

    def clean(self):
        if len(self.suffering_level) > 50:
            raise ValidationError("O nível de sofrimento não pode exceder 50 caracteres.")

    def __str__(self):
        return f"Questionnaire by {self.user.username} on {self.response_date}"

# Modelo para armazenar as respostas individuais
class Answer(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    question_number = models.IntegerField()
    
    # Alterei o campo 'answer' para CharField, para armazenar "Sim" ou "Não"
    answer = models.CharField(max_length=3, choices=[('Sim', 'Sim'), ('Não', 'Não')])

    def __str__(self):
        return f"Answer for Question {self.question_number} of {self.questionnaire.user.username}"