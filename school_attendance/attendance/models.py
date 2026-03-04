#models page
import uuid
import qrcode 
from io import BytesIO
from django.core.files import File
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class School(models.Model):
    udise_code = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=300)  

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.udise_code})"


class Classroom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="classrooms")
    grade = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    section = models.CharField(max_length=3, default="A")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["school", "grade", "section"],
                name="uniq_class_in_school",
            )
        ]
        ordering = ["school__name", "grade", "section"]

    def __str__(self):
        return f"Class {self.grade}{self.section} - {self.school.name}"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=50, unique=True)
    assigned_classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.employee_id})"


class Student(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="students")
    roll_number = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    qr_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.qr_code_image:
            qr_img = qrcode.make(str(self.qr_code))
            canvas = BytesIO()
            qr_img.save(canvas, format='PNG')
            canvas.seek(0)
            self.qr_code_image.save(f'{self.roll_number}_qr.png', File(canvas), save=False)
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["classroom", "roll_number"],
                name="uniq_roll_in_class",
            )
        ]
        ordering = ["classroom", "roll_number"]

    def __str__(self):
        return f"{self.roll_number} - {self.name} ({self.classroom})"


class Attendance(models.Model):
    ATTENDANCE_STATUS = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('ML', 'Medical Leave'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=2, choices=ATTENDANCE_STATUS)
    marked_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'date')  # one record per student per day

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"
