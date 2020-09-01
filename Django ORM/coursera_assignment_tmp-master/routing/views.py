from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,Http404,HttpResponseBadRequest


@csrf_exempt
@require_GET
def simple_route(request):
    return HttpResponse('')


@csrf_exempt
def slug_route(request, slug):
    return HttpResponse(str(slug))


@csrf_exempt
def sum_route(request, a, b):
    res = 0
    try:
        res = int(a) + int(b)
    except ValueError:
        raise Http404

    return HttpResponse(str(res))


@csrf_exempt
@require_GET
def sum_get_method(request):
    res = 0
    try:
        a = request.GET['a']
        b = request.GET['b']
        res = int(a) + int(b)
    except:
        return HttpResponseBadRequest()

    return HttpResponse(str(res))



@csrf_exempt
@require_POST
def sum_post_method(request):
    res = 0
    try:
        a = request.POST['a']
        b = request.POST['b']
        res = int(a) + int(b)
    except:
        return HttpResponseBadRequest()

    return HttpResponse(str(res))
