from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
import csv, io
from pathlib import Path
from datetime import date

# Create your views here.

BASE_DIR = Path(__file__).resolve().parent

all_posts = [
    {
        "slug": "chat-jacke",
        "image": "jacke.png",
        "author": "Haris",
        "date": date(2021, 7, 21),
        "title": "Test",
        "desc": "CLAUDIE PIERLOT Jacke silberfarben"
    },
    {
        "slug": "chat-mantel",
        "image": "mantel.png",
        "author": "Haris",
        "date": date(2022, 3, 10),
        "title": "Dieses Kleid von Ana Alcazar ist der perfekte Begleiter für jeden Casual Anlass.\nDer Basic Style wird durch ein grafisches Muster aufgewertet, während die Passform und der Schnitt einen Straight Fit bieten. Der Rundhals Ausschnitt wird durch Knöpfe verschlossen und der Rock fällt in Midirock Länge. Die Ärmel sind lang und machen das Kleid zu einem idealen Begleiter für Damen",
        "desc": "DUVETICA Daunenmantel \"Albaldah\" beige",
        "content": """INPUT
        Create a product description in german for an online shop using following attributes: 
        Produkt Typen : Kleid
        Zielgruppen : Damen
        Marke : Ana Alcazar
        Verschluss : mit Knöpfen
        Ausschnitt / Kragenform : mit Rundhals Ausschnitt
        Passform / Schnitt : Straight Fit
        Musterung : mit grafischem Muster
        Rocklänge : In Midirock Länge
        Ärmellänge : mit Langarm
        Stilrichtung : Basic Style
        Thematik ## Fashion : für den Casual Anlass
        """
    },
    {
        "slug": "chat-daunenjacke",
        "image": "daunenjacke.png",
        "author": "Haris",
        "date": date(2020, 8, 5),
        "title": "Test",
        "desc": "MACKAGE Daunenjacke \"Evie-Omb\" orange"
    }
]

def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        for ind, file in enumerate(request.FILES.getlist("file")):
            with open(BASE_DIR / "in" / f"{ind}.json", "wb") as f:
                for chunk in file.chunks():
                    f.write(chunk)
            with open(BASE_DIR / "out" / "chat.csv") as f:
                reader = csv.reader(f)
                next(reader)
                output = io.StringIO()
                writer = csv.writer(output)
                headers = {
                    "Onlineshop": 0,
                    "Akeneo Interne ID": 1,
                    "Input": 2,
                    "Output": 3,
                    "Creativity Parameter": 4
                }
                for ind, row in enumerate(reader):
                    output.write(row[3])
        return render(request, "blog/all-posts.html", {
            "all_posts": all_posts
            })
    else:
        form = UploadFileForm()
    return render(request, "blog/upload.html", {"form": form})


def get_date(post):
  return post['date']


def starting_page(request):
    sorted_posts = sorted(all_posts, key=get_date)
    latest_posts = sorted_posts[-3:]
    return render(request, "blog/index.html", {
      "posts": latest_posts
    })


def posts(request):
    return render(request, "blog/all-posts.html", {
      "all_posts": all_posts
    })


def post_detail(request, slug):
    identified_post = next(post for post in all_posts if post['slug'] == slug)
    return render(request, "blog/post-detail.html", {
      "post": identified_post
    })

