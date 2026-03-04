#serializer page
from rest_framework import serializers
from .models import Attendance, Student, Teacher
from django.utils import timezone

class AttendanceMarkSerializer(serializers.Serializer):
    qr_code = serializers.CharField()  # use CharField instead of UUIDField
    status = serializers.ChoiceField(choices=Attendance.ATTENDANCE_STATUS, default='P')

    def validate(self, data):
        qr_code = data.get('qr_code')
        try:
            student = Student.objects.get(qr_code=qr_code)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student with this QR code does not exist.")

        user = self.context['request'].user
        try:
            teacher = user.teacher
        except Teacher.DoesNotExist:
            raise serializers.ValidationError("Logged in user is not associated with any teacher account.")

        if teacher.assigned_classroom != student.classroom:
            raise serializers.ValidationError("You can only mark attendance for your assigned classroom.")

        data['student'] = student
        data['teacher'] = teacher
        return data

    def create(self, validated_data):
        student = validated_data['student']
        status = validated_data['status']
        teacher = validated_data['teacher']
        today = timezone.now().date()

        attendance, created = Attendance.objects.update_or_create(
            student=student,
            date=today,
            defaults={'status': status, 'marked_by': teacher}
        )
        return attendance
