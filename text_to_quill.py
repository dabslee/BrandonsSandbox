from blog.models import Post
import django_quill

for post in Post.objects.all():
    try:
        try:
            oldstr = post.content.html
        except:
            oldstr = post.content.json_string
        newstr = post.content.json_string
        newstr = newstr.replace("\"","\'")
        newstr = newstr.replace("\r","")
        newstr = newstr.replace("\n","")
        thestr = "{\"delta\":\"\",\"html\":\"" + newstr + "\"}"
        post.content.json_string = thestr
        post.save()
    except:
        pass