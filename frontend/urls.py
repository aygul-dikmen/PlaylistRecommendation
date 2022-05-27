from django.urls import path
from .views import *
app_name = 'frontend'
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name=''),
    path('my-playlists', index),
    path('recommendation', index),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
