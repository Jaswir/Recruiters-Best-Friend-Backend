from django.http import JsonResponse

def hello_world(request):
    d = {"name":"Gul Hassan"}
    return JsonResponse(d)