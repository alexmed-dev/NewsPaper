from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import PostCategory

from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives

from django.conf import settings
 

def get_subscribers(category):
    user_emails=[]
    for user in category.subscribers.all():
        user_emails.append(user.email)
    return user_emails


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    if kwargs['action']=='post_add':
         new_post_subscribers(instance) # так почта пользователей указывается массивом, но нет возможности обратиться к конкретному пользователю в письме (подходит для общих рассылок)
         new_post_subscribers_user(instance) # так в письме будет указано имя пользователя


def new_post_subscribers(instance):
    template='new_post.html'

    for category in instance.postCategory.all():
        email_subject=f"Новая статья в категории: {category}"
        user_emails=get_subscribers(category)
        html_content=render_to_string(
            template_name=template,
            context={
                'category': category,
                'post': instance,
            }
        ) 
        msg = EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=user_emails,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()



def new_post_subscribers_user(instance):
    template='new_post.html'

    for category in instance.postCategory.all():
        email_subject=f"Новая статья в категории: {category}"
        # для каждого пользователя отпраляем письмо отдельно - чтобы указать его имя
        for user in category.subscribers.all():
            html_content=render_to_string(
                template_name=template,
                context={
                    'category': category,
                    'post': instance,
                    'user': user,
                }
            )

            msg = EmailMultiAlternatives(
                subject=email_subject,
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email,],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
