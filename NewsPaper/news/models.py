from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.

class Author (models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.all().aggregate(pRat=Sum('postRating'))
        comRat = self.authorUser.comment_set.all().aggregate(cRat=Sum('commentRating'))
        #comPostRat = self.post_set.all().comment_set.all().aggregate(c_pRat=Sum('rating'))
        comPostRat = Comment.objects.filter(post__author = self).aggregate(c_pRat=Sum('commentRating'))
        self.rating = postRat.get('pRat')*3 + comRat.get('cRat') + comPostRat.get('c_pRat')
        self.save()

    def __str__(self):
        return f'Автор: {self.authorUser.username}'

class Category (models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers=models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.name}'
    

class Post (models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article='AR'
    news='NW'
    POST_TYPES=[
        (article, 'Статья'),
        (news,'Новость')
    ]
    postType=models.CharField(max_length=2, choices=POST_TYPES, default=news)
    dateTimeCreate=models.DateTimeField(auto_now_add=True)
    postCategory=models.ManyToManyField(Category, through='PostCategory')
    title=models.CharField(max_length=255)
    text=models.TextField()
    postRating=models.IntegerField(default=0)
    
    def like(self):
        self.postRating += 1
        self.save()

    def dislike(self):
        self.postRating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    def __str__(self):
        return f'{self.title}: {self.preview()}'
    
    def get_absolute_url(self): # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с новостью/статьей
        return f'/news/{self.id}' 
    

class PostCategory (models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment (models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    text=models.TextField()
    dateTimeCreate=models.DateTimeField(auto_now_add=True)
    commentRating=models.IntegerField(default=0)
    
    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating -= 1
        self.save()

    def __str__(self):
        return f'{self.text}'
    