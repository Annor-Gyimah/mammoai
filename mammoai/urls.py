
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),

    # customs urls
    
    path('user/', include('userauths.urls')),
    path('', include('home.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('dashboard/', include("user_dashboard.urls")),
    
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)