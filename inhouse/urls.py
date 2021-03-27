from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("newcase", views.newcase, name="newcase"),
    path("jobs", views.applyingjob, name="jobs"),
    path("query", views.query, name="query"),
    path("q/<int:casecode>", views.getCase, name="case"),
    path("changetheresbonsible", views.changer, name="changer"),
] 
 