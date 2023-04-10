from django.forms import ModelForm
from .models import Task
# Para crear un form personalizado, debemos crear dentro de nuestra app un archivo form.py y dentro de el ponemos el modelo en el cual se va a basar para realizar el form

class CreateTask(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority']