from django.shortcuts import render
import requests
from django.core.cache import cache
# from .tasks import notify_customers


# def say_hello(request):
#     notify_customers.delay('Hello')
#     return render(request, 'hello.html', {'name': 'Yann'})

def say_hello(request):
    key = 'httpbin_result'
    if cache.get(key) is None:
        response = requests.get("https://httpbin.org/delay/2")
        data = response.json()
        cache.set(key, data)
    return render(request, 'hello.html', {'name': cache.get(key)})
