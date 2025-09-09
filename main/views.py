from django.shortcuts import render

def home(request):
    context = {
        "app_name": "Football Shop",     # Application name
        "your_name": "Cristian Dillon Philbert",  # Your name
        "your_class": "Information system 2024"        # Your class
    }
    return render(request, ".html", context)
