from travello.models import Destination
from django.shortcuts import render

# Create your views here.
def index(request):

    # dest1 = Destination()
    # dest1.name = "Mumbai"
    # dest1.description = "The city which never sleeps"
    # dest1.price = 900
    # dest1.img = "destination_1.jpg"
    # dest1.offer = False

    # dest2 = Destination()
    # dest2.name = "Delhi"
    # dest2.description = "The city with best street food in India"
    # dest2.price = 800
    # dest2.img = "destination_2.jpg"
    # dest2.offer = False

    # dest3 = Destination()
    # dest3.name = "Hyderabad"
    # dest3.description = "First Biryani, Then Sherwani"
    # dest3.price = 700
    # dest3.img = "destination_3.jpg"
    # dest3.offer = False

    # dest4 = Destination()
    # dest4.name = "Chennai"
    # dest4.description = "The city for which Dhoni plays IPL"
    # dest4.price = 800
    # dest4.img = "destination_4.jpg"
    # dest4.offer = False

    # dest5 = Destination()
    # dest5.name = "Kolkata"
    # dest5.description = "The city with best sweets"
    # dest5.price = 600
    # dest5.img = "destination_5.jpg"
    # dest5.offer = True

    # dest6 = Destination()
    # dest6.name = "Bengaluru"
    # dest6.description = "Silicon valley of India"
    # dest6.price = 900
    # dest6.img = "destination_6.jpg"
    # dest6.offer = False

    # dests = [dest1, dest2, dest3, dest4, dest5, dest6]

    dests = Destination.objects.all()

    return render(request, 'index.html', {'dests':dests})