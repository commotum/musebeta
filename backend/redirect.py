from django.http import HttpResponseRedirect, HttpRequest


def images_redirect(req: HttpRequest, image: str):
    return HttpResponseRedirect('/_next/images/' + image)