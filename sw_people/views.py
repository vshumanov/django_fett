from django.shortcuts import render, redirect

from sw_people.forms import ValueCountsForm
from sw_people.services import (
    fetch_all_files,
    fetch_latest_characters,
    view_file,
    get_value_counts,
)


def index(request):
    return render(request, "index.html", {"files": fetch_all_files()})


def fetch(request):
    fetch_latest_characters()
    return render(request, "index.html", {"files": fetch_all_files()})


def file(request, filename, page):
    # TODO: not a fan of having 2 functionalities in a single view
    allow_load_more = True
    if request.method == "POST":
        form = ValueCountsForm(request.POST)
        if form.is_valid():
            headers = form.cleaned_data.get("headers_field")
            data, header = get_value_counts(filename, headers)
            allow_load_more = False
    else:
        data, header = view_file(filename, page)
        form = ValueCountsForm()

    return render(
        request,
        "file.html",
        {
            "data": data,
            "filename": filename,
            "header": header,
            "next_page": page + 1,
            "form": form,
            "allow_load_more": allow_load_more,
        },
    )
