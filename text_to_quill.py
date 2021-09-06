for sub in Submission.objects.all():
    try:
        try:
            oldstr = sub.details.html
        except:
            oldstr = sub.details.json_string
        newstr = ""
        for line in oldstr.replace("\r","").replace("\n","   ").split("   "):
            if not "<p>" in newstr:
                newstr += f"<p>{line}</p>"
            else:
                newstr += line
        newstr = newstr.replace("\"","\'")
        thestr = "{\"delta\":\"\",\"html\":\"" + newstr + "\"}"
        sub.details.json_string = thestr
        sub.save()
    except:
        pass