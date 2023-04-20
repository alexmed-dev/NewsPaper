from django_filters import FilterSet # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post
 
 
# создаём фильтр
class PostFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т.е. подбираться) информация
    class Meta:
        model = Post
        
        fields = {
            'author': ['exact'],
            'title': ['icontains'],
            'dateTimeCreate': ['date__gt' ],
        }
        