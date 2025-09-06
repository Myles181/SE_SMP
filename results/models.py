from django.db import models
from accounts.models import Student
from courses.models import Course

class Result(models.Model):
    GRADE_CHOICES = (
        ('A+', 'A+'),
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('C-', 'C-'),
        ('D+', 'D+'),
        ('D', 'D'),
        ('F', 'F'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'course', 'semester', 'year')
    
    def __str__(self):
        return f"{self.student} - {self.course} - {self.grade}"
    
    @property
    def percentage(self):
        return (self.marks_obtained / self.total_marks) * 100
