from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.text import Truncator
from .models import Post, Tag
from django.core import serializers
from django.http import HttpResponse
import json
import re

def entry_years():
    """Years with at least one post or project, newest first, for the sidebar's year tags."""
    years = {date.year for date in Post.objects.values_list('created', flat=True)}
    # Projects live in a shared template (so {% static %} works), not the database.
    projects_json = re.search(r'>(.*)</script>', render_to_string("projects_data.html"), re.S).group(1)
    years.update(int(project["date"][:4]) for project in json.loads(projects_json))
    return sorted(years, reverse=True)

# Create your views here.
def index(request, page=None):
    # Search, tag filtering and pagination all happen client-side. Old /blog/<page> links counted
    # pages from the newest end, which no longer matches, so send them to the default page.
    if page is not None:
        return redirect('blog:index')
    tags = Tag.objects.all()
    posts = [
        {
            "title": post.title,
            "date": post.created.isoformat(),
            "url": reverse('blog:post', args=[post.id]),
            "preview": Truncator(post.content.html).words(75, html=True),
            "text": strip_tags(post.content.html),
            "tags": [tag.name for tag in post.tags.all()],
        }
        for post in Post.objects.prefetch_related('tags').order_by('-created')
    ]
    return render(request, "index.html", {"posts": posts, "tags": tags, "years": entry_years()})

def post(request, postid):
    tags = Tag.objects.all()
    post = Post.objects.get(id=postid)
    return render(request, "post.html", {"post":post, "tags":tags, "years": entry_years()})

def allposts(request):
    posts = Post.objects.all()
    output = serializers.serialize('json', posts)
    output = json.dumps(json.loads(output), indent=4)
    return HttpResponse(output, content_type="application/json")
