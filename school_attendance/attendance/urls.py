#urls.page
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView #type:ignore
from .views import MarkAttendanceView,attendance_page  

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('mark-attendance/', MarkAttendanceView.as_view(), name='mark_attendance'),  
    path('attendance/', attendance_page, name='attendance_page'),
     
]
