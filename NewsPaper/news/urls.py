from django.urls import path
from .views import * # импортируем наше представление
from .views import upgrade_me
 
 
urlpatterns = [
    # path — означает путь
    path('', PostList.as_view()), # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>', PostDetail.as_view()),
    path('add', PostCreate.as_view()),
    path('<int:pk>/edit', PostUpdate.as_view()),
    path('<int:pk>/delete', PostDelete.as_view()),
    path('search', PostSearch.as_view()),
    path('profile', ProfileView.as_view()),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('category/<int:pk>/', PostCategory.as_view(), name = 'category'),
    path('subscribe/<int:pk>/', subscribe_to_category, name = 'subscribe'),
    path('unsubscribe/<int:pk>/', unsubscribe_from_category, name = 'unsubscribe'),
]