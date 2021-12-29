from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from evangelisation import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("accounts.urls")),
    path('', 
        views.notification_app_index, 
        name="notification_app_index"
    ),
    path('anniversaire/', include("evangelisation.urls")),
]

urlpatterns += static(settings.STATIC_URL,   document_root=settings.STATIC_ROOT)
#urlpatterns += static(settings.MEDIA_URL,   document_root=settings.MEDIA_ROOT)
