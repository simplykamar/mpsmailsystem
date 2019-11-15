from django.urls import path
from . import views
urlpatterns = [
	path('',views.home),
    path('home/',views.home),
    path('create/',views.create),
    path('sentmail/',views.sentmail),
    path('inbox/',views.inbox),
    path('inbox_view/<int:id>',views.inbox_view),
    path('sentmail_view/<int:id>',views.sentmail_view),
    path('notification',views.notification),
    path('delete_inbox/<int:id>',views.delete_inbox),
    path('delete_sent_mail/<int:id>',views.delete_sent_mail),
    path('save_starred/',views.save_starred),
    path('starred/',views.starred),
    path('delete_starred/',views.delete_starred),
    path('about/',views.about)

]
