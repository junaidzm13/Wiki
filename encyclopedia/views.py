from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import random

from . import util

class NewTaskForm(forms.Form):
    title = forms.CharField()

def index(request):
    if request.method == "POST":
        lst = util.list_entries()
        entry = request.POST.get('q')
        return HttpResponseRedirect(f"/search/{entry}")
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    if request.method == "POST":
        lst = util.list_entries()
        entry = request.POST.get('q')
        return HttpResponseRedirect(f"/search/{entry}")
    entries = util.list_entries()
    if title not in entries:
        return render(request, "encyclopedia/error.html", {
            "message": "No entry with that title!"
        })
    entry=util.get_entry(title)
    markdowner=Markdown()
    entry=(markdowner.convert(entry))
    return render(request, "encyclopedia/title.html", {
        "title_content": entry, "title": title
    })


def search(request, query):
    if request.method == "POST":
        lst = util.list_entries()
        entry = request.POST.get('q')
        return HttpResponseRedirect(f"/search/{entry}")
    lst = util.list_entries()
    if query in lst:
        return HttpResponseRedirect(f"/wiki/{query}")
    lst2 = []
    isvalid = False
    for item in lst:
        if query in item:
            lst2.append(item)
            isvalid = True
    if isvalid == False:
        return render(request, "encyclopedia/error.html", {
            "message": "No result for the used query"
        })
    else:
        return render(request, "encyclopedia/search.html", {
            "entries": lst2
        })


def newpage(request):
    if request.method == "POST":
        if "q" in request.POST:
            query = request.POST.get("q")
            return HttpResponseRedirect(f"/search/{entry}")
        else:
            title = request.POST.get('title')
            content = request.POST.get('content')
            entries = util.list_entries()
            for entry in entries:
                if entry == title:
                    return render(request, "encyclopedia/error.html", {
                        "message": "Entry already exists"
                    })
            f = open(f"entries/{title}.md", "w+")
            f.write(content)
            f.close()
            return HttpResponseRedirect(f"/wiki/{title}")
    return render(request, "encyclopedia/newpage.html")

def editpage(request, title):
    if request.method == "POST":
        if "q" in request.POST:
            query = request.POST.get("q")
            return HttpResponseRedirect(f"/search/{entry}")
        
        content = request.POST.get('content')
        f = open(f"entries/{title}.md", "w+")
        f.write(content)
        f.close()
        return HttpResponseRedirect(f"/wiki/{title}")
    
    content = util.get_entry(title)
    return render(request, "encyclopedia/editpage.html", {
        "content": content, "title": title
    })

def randompage(request):
    entries = util.list_entries()
    rand_number = random.randint(0, len(entries) - 1)
    entry = str(entries[rand_number])
    print(entry)
    return HttpResponseRedirect(f"/wiki/{entry}")