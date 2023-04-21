from django.shortcuts import render
# from django.views import View # импортируем простую вьюшку
# from django.core.paginator import Paginator # импортируем класс Paginator

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import *
from .filters import PostFilter # импортируем фильтр
from .forms import PostForm


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


# class PostDetail(DetailView):
#     model = Post # модель всё та же, но мы хотим получать детали конкретно отдельного товара
#     template_name = 'post.html' # название шаблона будет post.html
#     context_object_name = 'post' # название объекта

# дженерик для получения деталей о товаре
class PostDetail(DetailView):
    template_name = 'post.html'
    queryset = Post.objects.all()
 
 
# дженерик для создания объекта. Надо указать только имя шаблона и класс формы который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreate(CreateView):
    template_name = 'post_create.html'
    form_class = PostForm


# дженерик для редактирования объекта
class PostUpdate(UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm
 
    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
 
 
# дженерик для удаления объекта
class PostDelete(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '../'