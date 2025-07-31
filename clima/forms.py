from django import forms

class CiudadForm(forms.Form):
    nombre = forms.CharField(label='Nombre de la ciudad', max_length=100)
    pais = forms.ChoiceField(
        label='Código del país',
        choices=[
            ('CL', 'Chile'),
            ('AR', 'Argentina'),
            ('US', 'Estados Unidos'),
            ('ES', 'España'),
            ('PE', 'Perú'),
            ('MX', 'México'),
            ('BR', 'Brasil'),
            ('CO', 'Colombia'),
        ]
    )
