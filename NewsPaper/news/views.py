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


from pydoc import resolve
# from django.core.exceptions import ObjectDoesNotExist

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string # импортируем функцию, которая срендерит наш html в 

from django.conf import settings
DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL

from datetime import datetime


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
    # # form_class.limit=1
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)        
    #     user = self.request.user
    #     posts=Post.objects.filter(dateTimeCreate__date__gt=datetime.today(), author__authorUser__exact=user)
    #     context['limit'] = posts.count
    #     return context

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
        # добавим список категорий, на которые подписан пользователь
        user = self.request.user
        categories = Category.objects.filter(subscribers=user)
        context['categories'] = categories

        return context
    

class PostCategory(ListView):
    model = Post
    template_name = 'category.html'
    context_object_name = 'posts'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-id') # это если без формы поиска
    ordering = ['-dateTimeCreate']
    # paginate_by = 10
    
    def get_queryset(self):
        # self.id = resolve(self.request.path_info).kwargs['pk']
        # cat = Category.objects.get(id=self.id)
        # queryset = Post.objects.filter(category=cat)
        # # queryset.category = cat
        # return queryset

        id = self.kwargs.get('pk')
        cat = Category.objects.get(pk=id)
        queryset = Post.objects.filter(postCategory=cat)
        queryset.category = cat
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        id = self.kwargs.get('pk')
        category = Category.objects.get(pk=id)
        if category:
           context['category'] = category
        else:
            context['category'] = False
        if hasattr(user, 'email'):  # подписаться могут только авторизованные пользователи (у них есть user.email)
            subscribed = category.subscribers.filter(email=user.email)
            context['not_subscribed'] = not subscribed
        # if not subscribed:
        #     context['category']['not_subscribed'] = category
        # context['category'] = False
        return context
    

@login_required
def subscribe_to_category(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)

    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        html_content = render_to_string( 
            'subscribed.html',
            {
                'categories': category,
                'user': user,
            }
        )
            
        msg = EmailMultiAlternatives(
            subject=f'добавлена категория {category.name}',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=[user.email,],
        )

        msg.attach_alternative(html_content, "text/html") # добавляем html
        msg.send()
        # try:
        #     msg.send() # отсылаем
        # except Exception as e:
        #     print(e)
 
        return redirect('/news')
    

@login_required
def unsubscribe_from_category(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)

    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)

        return redirect('/news')
