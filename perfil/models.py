from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
import re


class Endereco(models.Model):
    rua = models.CharField(max_length=20)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=20, blank=True, null=True)
    bairro = models.CharField(max_length=20)
    cep = models.CharField(max_length=20)
    cidade = models.CharField(max_length=20)
    estado = models.CharField(
        default='DF',
        max_length=2,
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def __str__(self):
        return f'{self.rua}, {self.numero} - {self.bairro}'

    def clean(self):

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            pass

    class Meta:
        verbose_name = "Endereço"


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
