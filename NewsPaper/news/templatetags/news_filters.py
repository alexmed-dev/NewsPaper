from django import template
from .bad_words import bad_words_list
 
register = template.Library() # если мы не зарегестрируем наши фильтры, то django никогда не узнает где именно их искать и фильтры потеряются

@register.filter(name='censor') # регистрируем наш фильтр под именем censor, чтоб django понимал, что это именно фильтр, а не простая функция
def censor(value): # первый аргумент здесь — это то значение, к которому надо применить фильтр, т.е. примерно следующее будет в шаблоне value|censor
    for word in bad_words_list:
        value = value.replace(word, "")
    return value # возвращаемое функцией значение — это то значение, которое подставится к нам в шаблон
