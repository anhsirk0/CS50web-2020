import glob, random
import markdown2
from django.shortcuts import render, redirect
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, name):
    ls = glob.glob("entries/*.md")
    html = f"<h1>Entry page for '{name}' does not not exist</h1>"
    for item in ls:
        file = item.lower().split("/")[-1]
        if name.lower() == file.split(".")[0]:
            content = open(item).read()
            html = markdown2.markdown(content)
            return render(request, "encyclopedia/entry.html", {"content": html, "title": name})
    return HttpResponse(html)


def search(request):
    q = request.GET.get('q')
    query = q.lower()
    ls = glob.glob("entries/*.md")
    new = []
    for file in ls:
        name = file.split("/")[-1].split(".")[0]
        # exact match
        if query == name.lower():
            content = open(file).read()
            result = markdown2.markdown(content)
            return redirect(entry,name=query)

        # partial match
        l = len(query)
        n = len(name)
        if not l > n:
            for i in range(n - l+1):
                if query == name.lower()[i:i+l]:
                    new.append(name)
                    break

    if new:
        content = f"<h1>Search Results for ' {q} '</h1>"
        return render(request, "encyclopedia/search.html", {"content": content,"entries": new})

        # no match
    result = f"<h1>No match found for ' {q} '</h1>"
    return render(request, "encyclopedia/search.html", {"content": result})

def new(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        title = title[0].upper()+title[1:]
        content = request.POST.get('content')
        util.save_entry(title, content)
        return redirect(entry,name=title)
    entries = util.list_entries()
    page_title = "New - Encyclopedia"
    return render(request, "encyclopedia/new.html", {
        "page_title": page_title ,
        "entries": entries
    })

def edit(request):
    title = request.GET.get("title")
    content = util.get_entry(title)
    entries = util.list_entries()
    entries.remove(title)
    page_title = f"Edit - {title}  - Encyclopedia"
    return render(request, "encyclopedia/edit.html", {
        "entries": entries,
        "page_title": page_title,
        "title": title,
        "content": content
    })

def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return redirect(entry,name=title)
