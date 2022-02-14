from django.contrib import admin
from .models import Student, Course

class StudentAdmin(admin.ModelAdmin):
    pass

class CourseAdmin(admin.ModelAdmin):
    pass

admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)

