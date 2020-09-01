from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def echo(request):
    #print(request.META)
    context = {}
    if request.method == "GET":
        context['params'] =list(request.GET.items())
        context['method'] ="get"
    elif request.method == 'POST':
        context['params'] = list(request.POST.items())
        context['method'] ="post"

    context['is_empty'] = not bool(context['params'])

    context['statement'] = request.META['HTTP_X_PRINT_STATEMENT'] if 'HTTP_X_PRINT_STATEMENT' in request.META else 'empty'

    #print(context)
    return render(request, 'echo.html', context, status= 200)


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 7),
        'b': request.GET.get('b', 2)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })
