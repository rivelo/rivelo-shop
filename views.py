from django.http import HttpResponse
import datetime
from django.shortcuts import render_to_response


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def main_page(request):
    
    return render_to_response("index.html", {"weblink": 'top.html'})
