from django.urls import path

from .views import * 



urlpatterns = [
    path("", home, name="home"),
    path("signin/", signin, name="signin"),
    path("register/", register, name="register"),
    path("signout/", signout, name="signout"),
    path("clientManagement/", clientManagement, name="clientManagement"),
    path("newClient/", newClient, name="newClient"),
    path("updateClient/<int:pk>/", updateClient, name="updateClient"),
    path("deleteClient/<int:pk>/", deleteClient, name="deleteClient"),
    path("clientInfo/<int:pk>/", clientInfo, name="clientInfo"),
    path("activeClient/", activeClient, name="activeClient"),
    path("closedClient/", closedClient, name="closedClient"),
    path("courtAttendances/<int:pk>/", courtAttendances, name="courtAttendances"),
    path("billing/", Billing, name="Billing"),
    path('charts/',charts,name='charts')
]