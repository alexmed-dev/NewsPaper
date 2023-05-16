import logging
 
from django.conf import settings
 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution


from datetime import datetime, timedelta
from news.models import Post, Category
# from models import Post
# import models
from django.contrib.auth.models import User


from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
 
logger = logging.getLogger(__name__)
 
 
# наша задача по выводу текста на экран
def my_job():
    #  Your job processing logic here... 
    print('hello from job')

# функция формирует и отправляет письма о новых (за прошедшую неделю) статьях в категориях с подпиской
def new_week_post_remind():
    template='new_week_posts.html'
    users=User.objects.all() # выбираем всех пользователей и для каждого (в цикле):
    for user in users:
        categories=Category.objects.filter(subscribers__exact=user) # отбираем категории, на которые подписан пользователь
        if categories: # если есть категории, формируем и отсылаем письмо:
            # отбираем посты созданные за последнюю неделю и из категорий, которые отобрали ранее и убираем повторы
            posts=Post.objects.filter(dateTimeCreate__date__gt=datetime.today()-timedelta(weeks=1), postCategory__in=categories).distinct()

            email_subject="Новые статьи в ваших любимых категориях"
            # user_emails=[user.email_user,]
            html_content=render_to_string(
                template_name=template,
                context={
                    'user': user,
                    'posts': posts,
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
            print("ok")

 
# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        # scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler = BlockingScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Тоже самое что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
        
        # добавляем еженедельную рассылку подписчикам ссылок на новые статьи
        scheduler.add_job(
            new_week_post_remind,
            # trigger=CronTrigger(second="*/10"),
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Каждую неделю будут высылаться уведомления о новых статьях в категориях с подпиской
            id="new_week_post_remind",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'new_week_post_remind'."
        )
 
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )


        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")