from django.urls import path
from django.contrib.auth import views as auth_views

from evangelisation import views



app_name="notification"


urlpatterns = [
    path('personnes', 
        views.notification_app_index, 
        name="notification_app_index"
    ),

    path('<str:type_opera>/personnes', 
        views.notification_app_ajouter_personne, 
        name="notification_app_ajouter_personne"
    ),

    path('<str:type_opera>/personnes/<int:pk>/detail', 
        views.notification_app_detail_personne, 
        name="notification_app_detail_personne"
    ),
    

    path('personnes/<int:pk>/<str:type_opera>', 
        views.notification_app_supprimer_personne, 
        name="notification_app_supprimer_personne"
    ),
            
]
