from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import Topic, Course, Student, Order, Review

class CourseAdmin(admin.ModelAdmin):
    fields = [('title'), ('price', 'num_reviews', 'for_everyone')]
    list_display = ('title', 'topic', 'price','topic_name','topic_length')
    actions = ["add_50_to_hours","sub_50_to_hours"]


    def add_50_to_hours(self, request, queryset):

        for obj in queryset:
            topic = obj.topic
            print("topic length=", topic.name, "=", topic.length)
            topic.length+=10
            print("topic length=",topic.name,"=",topic.length)
            topic.save()
            updated=queryset.update(topic=topic)
        self.message_user(request, ngettext(
                '%d course hours are increased by 10.',
                '%d courses hours are increased by 10.',
                updated,
            ) % updated, messages.SUCCESS)
    add_50_to_hours.short_description = "Add 10 hours"

    def sub_50_to_hours(self, request, queryset):

        for obj in queryset:
            topic = obj.topic
            print("topic length=", topic.name, "=", topic.length)
            topic.length -= 10
            print("topic length=", topic.name, "=", topic.length)
            topic.save()
            updated = queryset.update(topic=topic)
        self.message_user(request, ngettext(
            '%d course hours are decreased by 10.',
            '%d courses hours are decreased by 10.',
            updated,
        ) % updated, messages.SUCCESS)

    sub_50_to_hours.short_description = "Subtract 10 hours"

class StudentAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name']
    list_display = ('upper_case_name', 'address')

    

class OrderAdmin(admin.ModelAdmin):
    fields = [('courses','topic'), ('student', 'order_status', 'order_date')]
    list_display = ('id', 'Student', 'order_status', 'order_date', 'total_cost', 'total_items')



# Register your models here.
admin.site.register(Topic)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
