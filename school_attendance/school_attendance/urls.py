# school_attendance/urls.py

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf.urls.static import static
from django.conf import settings          

# Function to render the login page
def login_page(request):
    return render(request, 'login.html')  # make sure templates/login.html exists

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_page, name='login_page'),          # Login page at root URL
    path('api/', include('attendance.urls')),         # API endpoints (JWT & attendance)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)