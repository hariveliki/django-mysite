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
        "slug": "daunenjacke",
        "image": "daunenjacke.png",
        "author": "Haris",
        "date": date(2021, 7, 21),
        "title": """
        Diese stylische Daunenjacke für Damen der Marke MACKAGE macht stets eine gute Figur. Sie hat eine Regular Fit Passform und eine Rückenlänge von 53 cm. Der Verschluss ist ein praktischer Reissverschluss, während sich hinter dem Kapuzenkragen eine abnehmbare Kapuze verbirgt. Elastische Bündchen an den Armabschlüssen machen das Design komplett. Zudem verfügt die Jacke über ein farblich passendes Innenfutter und ein organischeres Muster. Für noch mehr Komfort sorgen die Reissverschlusstaschen sowie ein Fach mit Reissverschluss im Inneren. Mit ihrer Ärmellänge von 65 cm bietet diese Jacke ein tolles Trageerlebnis.
        """,
        "excerpt": "There's nothing like the views you get when hiking in the mountains! And I wasn't even prepared for what happened whilst I was enjoying the view!",
        "content": """
        INPUT:
        Create a product description in german for an online shop using following attributes: 
        Produkt Typen : Daunenjacke
        Zielgruppen : Damen
        Marke : MACKAGE
        Rückenlänge : 
        Verschluss : mit Reissverschluss
        Ausschnitt / Kragenform : mit Kapuzenkragen
        Armabschluss : Armabschluss mit elastischen Bündchen
        Passform / Schnitt : Regular Fit
        Kapuze : mit abnehmbarer Kapuze
        Innenausstattung : Innenausstattung mit Fach mit Reissverschluss
        Futter : mit farblich passendem Innenfutter
        Musterung : mit organischem Muster
        Taschen : mit Reissverschlusstaschen
        Ärmellänge : mit Langarm
        """,
        "foo": "",
        "boo": "MACKAGE Daunenjacke \"Evie-Omb\" orange"
    },
    {
        "slug": "jacke",
        "image": "jacke.png",
        "author": "Haris",
        "date": date(2022, 3, 10),
        "title": "Diese Jacke von CLAUDIE PIERLOT ist der perfekte Begleiter um dein Outfit zu vervollständigen! Der Regular Fit sorgt für einen angenehmen Tragekomfort und das Hahnentritt Gewebe mit typischer Musterung macht den Look stilvoll und trendy. Der Schnitt beeindruckt durch seinen Hemdkragen und die aufgesetzten Taschen, während der Verschluss durch Knöpfe unterstützt wird. Mit einer Länge von 1m72 und der Größe 36 ist dieses Modell das Richtige für dein neues Lieblingsstück im Stil des Trendstyle mit Karo Muster!",
        "excerpt": "Did you ever spend hours searching that one error in your code? Yep - that's what happened to me yesterday...",
        "content": """
        Create a product description in german for an online shop using following attributes: 
        Produkt Typen : Jacke
        Zielgruppen : Damen
        Marke : CLAUDIE PIERLOT
        Verschluss : mit Knöpfen
        Ausschnitt / Kragenform : mit Hemdkragen
        Beschreibung : Das Model ist 1m72 groß und trägt Größe 36
        Passform / Schnitt : Regular Fit
        Musterung : mit Karo Muster
        Taschen : mit aufgesetzten Taschen
        Ärmellänge : mit Langarm
        Stilrichtung : Trend Style
        Webart : Hahnentritt Gewebe mit typischer Musterung
        """,
        "boo": "CLAUDIE PIERLOT Jacke silberfarben"
    },
    {
        "slug": "mantel",
        "image": "mantel.png",
        "author": "Haris",
        "date": date(2020, 8, 5),
        "title": """
        Der Duvetica Damen Daunenmantel ist ein Must-Have für jede Fashionista. Er verfügt über einen Stehkragen und einen Reissverschluss, sowie zwei Reissverschlusstaschen. Der Mantel hat ein unifarbenes Design, eine Wassersäule von 10.000 mm und langem Arm. Machen Sie Ihren Look komplett mit dem stilvollen Damen Daunenmantel von Duvetica!
        """,
        "excerpt": "-",
        "content": """
        Create a product description in german for an online shop using following attributes: 
        Produkt Typen : Daunenmantel
        Zielgruppen : Damen
        Marke : Duvetica
        Verschluss : mit Reissverschluss
        Ausschnitt / Kragenform : mit Stehkragen
        Musterung : Unifarben
        Taschen : mit Reissverschlusstaschen
        Ärmellänge : mit Langarm
        Ausstattung ## Fashion : ist Wasserabweisend
        """,
        "boo": "DUVETICA Daunenmantel \"Albaldah\" beige"
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

