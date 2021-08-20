from django.shortcuts import render
from .models import Post, Tag
from django.core import serializers
from django.http import HttpResponse
import json
from django.db.models import Q

import math

# Create your views here.
def index(request, page=1):
    tags = Tag.objects.all()
    if request.method == 'POST':
        query=None
        selected_tag_id = None
        posts = Post.objects.all().order_by('id').reverse()
        if "searchbar" in request.POST:
            query = request.POST['searchbar']
            posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
        tagfilter = None
        for tag in Tag.objects.all():
            if f"filter-submit-{tag.id}" in request.POST:
                tagfilter = tag
                selected_tag_id = tag.id
                break
        if tagfilter:
            posts = posts.filter(Q(tags=tagfilter))
        return render(request, "index.html", {"posts":posts, "previous":0, "searchquery":query, "selected_tag_id":selected_tag_id, "tags":tags})
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
    tags = Tag.objects.all()
    post = Post.objects.get(id=postid)
    return render(request, "post.html", {"post":post, "tags":tags})

def allposts(request):
    posts = Post.objects.all()
    output = serializers.serialize('json', posts)
    output = json.dumps(json.loads(output), indent=4)
    return HttpResponse(output, content_type="application/json")
