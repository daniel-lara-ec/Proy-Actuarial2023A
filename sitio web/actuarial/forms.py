from django import forms 

class FormularioSeguro(forms.Form):
    edad = forms.IntegerField(label='Edad', min_value=0, max_value=100)
    sexo = forms.ChoiceField(label='Sexo', choices=[('M', 'Masculino'), ('F', 'Femenino')])
    cobertura_fallecimiento = forms.IntegerField(label='Cobertura (Fallecimiento)', min_value=0, max_value=100)
    cobertura_supervivencia = forms.IntegerField(label='Cobertura (Supervivencia)', min_value=0, max_value=100)
    cuantia = forms.FloatField(label='Cuantia', min_value=0, max_value=10000000)
    interes = forms.FloatField(label='Interes', min_value=0, max_value=100)