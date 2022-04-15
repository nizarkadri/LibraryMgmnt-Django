from django.db import models
from django.db.models import Sum

import datetime
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)
    length = models.IntegerField(default=12, blank=False)

    def __str__(self):
        return '%s' % (self.name)


class Course(models.Model):
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    # topic= models.ManyToManyField(Topic, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(blank= True)
    num_reviews = models.PositiveIntegerField(default=0)

    def topic_length(self):
        return str(self.topic.length)
    def topic_name(self):
        return str(self.topic.name)

    def __str__(self):
        return '%s' % (self.title)

class Student(User):
    LVL_CHOICES = [
    ('HS', 'High School'),
    ('UG', 'Undergraduate'),
    ('PG', 'Postgraduate'),
    ('ND', 'No Degree'),
    ]
    level = models.CharField(choices=LVL_CHOICES, max_length=2, default='HS')
    address = models.CharField(max_length=300)
    province=models.CharField(max_length=2, default='ON')
    registered_courses = models.ManyToManyField(Course, blank=True)
    interested_in = models.ManyToManyField(Topic)
    address = models.CharField(max_length=100, blank=False)

    def upper_case_name(self):
        return ('%s %s' % (self.first_name,self.last_name)).upper()
    upper_case_name.short_description="Student Full Name"

    def __str__(self):
        return '%s' % self.username

class Order(models.Model):
    courses = models.ManyToManyField(Course)
    Student = models.ForeignKey(Student, name="Student", on_delete=models.CASCADE,default="john")
    order_values_map = [(0, 'Cancelled'), (1, 'Confirmed'), (2, 'On Hold')]
    order_status=models.IntegerField(default=1, choices=order_values_map)
    order_date = models.DateField(default=timezone.now)

    def total_cost(self):
        return '%s ordered courses worth %s' % (self.Student,self.courses.aggregate(
            total_price=Sum('price')
        )['total_price'])
    def total_items(self):
        return self.courses.count()

    def __str__(self):
        return self.total_cost()

class Review(models.Model):
    reviewer = models.EmailField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return "Reviewed by :%s \nFor Course:%s\nRating:%s\nComments:%s" % (self.reviewer,self.course,self.rating,self.comments)




