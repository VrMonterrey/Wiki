from django.shortcuts import render
from markdown2 import Markdown
import random
from . import util


def to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = to_html(title)
    if content == None:
        return render(request, "encyclopedia/error.html",{
            "message" : "The entry doesn't exist"
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "title" : title,
            "content" : content
        })
    
def search(request):
    if request.method == "POST":
        sear = request.POST['q']
        html = to_html(sear)
        if html != None:
            return render(request, "encyclopedia/entry.html",{
            "title" : sear,
            "content" : html
            })
        else:
            entries = util.list_entries()
            rec = []
            for entry in entries:
                if sear.lower() in entry.lower():
                    rec.append(entry)
            return render(request, "encyclopedia/search.html",{
                "rec" : rec
            })

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        ex = util.get_entry(title)
        if ex is not None:
            return render(request,"encyclopedia/error.html",{
                "message" : "The entry already exists"
            })
        else:
            util.save_entry(title,content)
            html = to_html(title)
            return render(request,"encyclopedia/entry.html",{
                "title" : title,
                "content" : html
            })

def edit(request):
    if request.method == "POST":
        title = request.POST["et"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title" : title,
            "content" : content
        })
    
def save(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        html = to_html(title)
        return render(request,"encyclopedia/entry.html",{
            "title" : title,
            "content" : html
        })
    
def random_page(request):
    all = util.list_entries()
    rand = random.choice(all)
    html = to_html(rand)
    return render(request,"encyclopedia/entry.html",{
            "title" : rand,
            "content" : html
        })
