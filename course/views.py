import json
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.http.response import HttpResponse
from .models import Course
from django.views.generic import TemplateView,ListView,CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from braces.views import LoginRequiredMixin
from .forms import CreateCourseForm

class AboutView(TemplateView):
    template_name="course/about.html"

class CourseListView(ListView):
    model=Course
    context_object_name = "courses"
    template_name = "course/course_list.html"


class UserMixin:
    def get_queryset(self):
        qs = super(UserMixin, self).get_queryset()
        return qs.filter(user=self.request.user)
    
class UserCourseMixin(UserMixin, LoginRequiredMixin):
    model=Course
    login_url = "/account/login/"

class ManageCourseListView(UserCourseMixin, ListView):
    context_object_name = "courses"
    template_name = "course/manage/manage_course_list.html"

class HisCourseListView(ListView):
    def get_queryset(self):
        qs = super(HisCourseListView, self).get_queryset()
        return qs.filter(user=User.objects.filter(username="tester1")[0])
    model=Course
    context_object_name = "courses"
    template_name = "course/course_list.html"
    
class CreateCourseView(UserCourseMixin, CreateView):
    # context_object_name = "courses"
    template_name = "course/manage/create_course.html"
    fields =["title", "overview"]

    def post(self, request, *args, **kwargs):
        form=CreateCourseForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = self.request.user
            new_course.save()
            return redirect("course:manage_course")
        return self.render_to_response({"form":form})


class DeleteCourseView(UserCourseMixin, DeleteView):
#    template_name = "course/manage/delete_course.html"
     success_url = reverse_lazy("course:manage_course")
     def dispatch(self, *args, **kwargs):
        resp = super(DeleteCourseView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result":"ok"}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return resp

class UpdateCourseView(UserCourseMixin, UpdateView):
     template_name = "course/manage/update_course.html"
     success_url = reverse_lazy("course:manage_course")
     fields =["title", "overview"]
