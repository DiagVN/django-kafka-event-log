from django.http import HttpResponse


def health_check(_request):
    return HttpResponse('ok')
