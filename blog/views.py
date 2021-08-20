from django.shortcuts import render
from .models import Post, Tag
from django.core import serializers
from django.http import HttpResponse
from django.http.response import JsonResponse
import json
from django.db.models import Q

import math

# Create your views here.
def index(request, page=1):
    tags = Tag.objects.all()
    if request.method == 'POST':
        query = request.POST['searchbar']
        print(query)
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('id').reverse()
        return render(request, "index.html", {"posts":posts, "previous":0, "searchquery":query, "tags":tags})
    else:
        page = int(page)
        posts = Post.objects.all().order_by('id').reverse()
        maxpage = math.ceil(len(posts)/7)
        posts = posts[7*(page-1):7*page]
        if page < maxpage:
            return render(request, "index.html", {"posts":posts, "previous":page+1, "tags":tags})
        else:
            return render(request, "index.html", {"posts":posts, "previous":0, "tags":tags})

def post(request, postid):
    post = Post.objects.get(id=postid)
    return render(request, "post.html", {"post":post})

def allposts(request):
    posts = Post.objects.all()
    output = serializers.serialize('json', posts)
    output = json.dumps(json.loads(output), indent=4)
    return HttpResponse(output, content_type="application/json")
