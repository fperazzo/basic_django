from django.db import models

from django.utils import timezone

# Create your models here

class TipoLivro(models.Model):
	nmtipolivro = models.CharField(max_length=30)
	def __str__(self):
		return f'{self.nmtipolivro}'

#Esta será sua entidade principal, aquela que é o centro da aplicação
class Livro(models.Model):

	nomelivro = models.CharField(max_length=10)

	numpaginas = models.FloatField()
	numvendas = models.FloatField(default=0,blank=True)

	autor = models.CharField(editable=False,max_length=10,default='teste')
	created = models.DateTimeField(editable=False)
	modified = models.DateTimeField(editable=False)
	

	def save(self, *args, **kwargs):
	    ''' On save, update timestamps '''
	    if not self.id:
	    	self.created = timezone.now()
	    self.modified = timezone.now()
	    return super(Livro, self).save(*args, **kwargs)

		def __str__(self):
		return  'Livro: '+ str(self.id) +' Titulo '+ str(self.nomelivro)

#Entidade Associativa - para evitar relações many-to-many

class Livro_TipoLivro(models.Model):
    idlivro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    idtipolivro = models.ForeignKey(TipoLivro, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.idlivro) +' op. '+ str(self.idtipolivro)

objects = models.Manager()

