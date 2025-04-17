from rest_framework import serializers
from .models import SRQ20Response

class SRQ20ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SRQ20Response
        fields = ['id', 'user', 'responses', 'submitted_at']

    def validate_responses(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("As respostas devem estar em um dicionário.")

        if len(value) != 20:
            raise serializers.ValidationError("Devem haver exatamente 20 perguntas no questionário.")

        for i in range(1, 21):
            key = f'question_{i}'
            if key not in value:
                raise serializers.ValidationError(f"'{key}' está faltando nas respostas.")
            if not isinstance(value[key], bool):
                raise serializers.ValidationError(f"O valor de '{key}' deve ser verdadeiro ou falso.")

        return value
