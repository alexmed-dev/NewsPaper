from django.shortcuts import render
# from django.views import View # импортируем простую вьюшку
# from django.core.paginator import Paginator # импортируем класс Paginator

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from .models import *
from .filters import PostFilter # импортируем фильтр
from .forms import PostForm


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import Group

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'posts.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'posts'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-id') # это если без формы поиска
    # ordering = ['-id'] # это если с формой поиска
    paginate_by = 10 # поставим постраничный вывод в 10 элементов

class PostSearch(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'search.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'posts'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    # queryset = Post.objects.order_by('-id') # это если без формы поиска
    ordering = ['-id'] # это если с формой поиска
    #paginate_by = 2 # поставим постраничный вывод в один элемент

    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context


# дженерик для получения деталей о товаре
class PostDetail(DetailView):
    template_name = 'post.html'
    queryset = Post.objects.all()
 
 
# дженерик для создания объекта. Надо указать только имя шаблона и класс формы который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'post_create.html'
    permission_required = ('news.add_post', )
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для редактирования объекта
class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    permission_required = ('news.change_post', )
    form_class = PostForm
 
    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
 
 
# дженерик для удаления объекта
class PostDelete(LoginRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '../'



@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')    
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news')


class ProfileView(LoginRequiredMixin, TemplateView):
    # template_name = 'account/profile.html'
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context