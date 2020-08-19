
#Criar modelos (TABELAS DO BANCO DE DADOS)


url.py do projeto

from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('', include('appp.urls', namespace='appp')),

    path('admin/', admin.site.urls),
]

apps.py do app

from django.apps import AppConfig


class ApppConfig(AppConfig):
    name = 'appp'

#Admin.py do app para incluir os models no /admin

from django.contrib import admin

# Register your models here.
from proj.models import Dimdata, Dimlocal, FRegistro, Publication

'''admin.site.register(Dimdata)
admin.site.register(Dimlocal)
admin.site.register(FRegistro)
admin.site.register(Publication)




python manage.py createsuperuser



No Django, os modelos são descritos no arquivo models.py. 
Ele já foi criado e está presente na pasta helloworld/models.py. 

Portanto, toda vez que você alterar o seu modelo, não se esqueça de executar:

python manage.py makemigrations projeto

Para que o Django as aplique, são necessárias três coisas, basicamente: 
 1. Que a configuração da interface com o banco de dados esteja descrita no settings.py 
 2. Que os modelos e migrations estejam definidos para esse projeto. 
 3. Execução do comando migrate 

Agora só falta executar o comando migrate, propriamente dito! 
Para isso, vamos para a raíz do projeto e executamos: 

python manage.py migrate


Com nossa classe Funcionário modelada, vamos agora ver a API de acesso à dados provida pelo Django para facilitar muito a nossa vida! Vamos testar a adição de um novo funcionário utilizando o shell do Django. Para isso, digite o comando: 1 

python manage.py shell

no shell:

from helloworld.models import Funcionario 

funcionario = Funcionario( 
nome='Marcos', 
sobrenome='da Silva', 
cpf='015.458.895-50', 
tempo_de_servico=5, 
remuneracao=10500.00 
) 

funcionario.save() '''
