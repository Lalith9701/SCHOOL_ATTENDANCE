from rest_framework.views import APIView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializer import AttendanceMarkSerializer


def attendance_page(request):
    return render(request, 'attendance_page.html')
    

class MarkAttendanceView(APIView):
    permission_classes = [IsAuthenticated]  # ensure user is logged in

    def post(self, request):
        serializer = AttendanceMarkSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            attendance = serializer.save()
            return Response({
                'message': 'Attendance marked successfully',
                'attendance_id': attendance.id,
                'student': attendance.student.name,
                'status': attendance.status,
                'date': attendance.date,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   