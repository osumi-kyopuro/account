from django.core.mail import send_mail
from django.http import HttpResponse

def mail(request):
    send_mail(
        'タイトル',
        '本文.',
        'osumiyuki1123@gmail.com',
        ['osumiyuki1123@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse('')