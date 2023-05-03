from django.forms import ModelForm
from .models import Post
 
from allauth.account.forms import SignupForm # для автоматического добавления нового пользователя в группу
from django.contrib.auth.models import Group #


# Создаём модельную форму
class PostForm(ModelForm):
    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'postCategory', 'postType']


class CommonSignupForm(SignupForm):
    
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user