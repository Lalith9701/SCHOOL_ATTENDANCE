from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf.urls.static import static
from django.conf import settings          

def login_page(request):
    return render(request, 'login.html')  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_page, name='login_page'),          
    path('api/', include('attendance.urls')),        
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
