from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse

from .models import ArticleColumn, ArticlePost
from .forms import ArticleColumnForm, ArticlePostForm

# Create your views here.
@login_required(login_url='/account/login/')
def article_column(request):
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request, "article/column/article_column.html", {"columns": columns, "column_form": column_form}) 
    elif request.method == "POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name)
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse('1')


@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST["column_name"]
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except Exception as e:
        print(e)
        return HttpResponse("0")


@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def delete_article_column(request):
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("1")
    except Exception as e:
        print(e)
        return HttpResponse("0")

@login_required(login_url='/account/login/')
@csrf_exempt
def article_post(request):
    if request.method == "POST":
        articlepost_form = ArticlePostForm(request.POST)
        if articlepost_form.is_valid():
            cd = articlepost_form.cleaned_data
            try:
                new_article = articlepost_form.save(commit=False)            
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST["column_id"]) 
                new_article.save()
                return HttpResponse("1")
            except Exception as e:
                print(e)
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    elif request.method == "GET":
        articlepost_form = ArticlePostForm()
        print(type(request.user))
        article_columns = request.user.article_column.all()
        return render(request, "article/column/article_post.html", {"article_columns":article_columns, "articlepost_form":articlepost_form})

@login_required(login_url='/account/login/')
def article_list(request):
    article_posts = ArticlePost.objects.filter(author=request.user)
    return render(request, "article/column/article_list.html", {"articles":article_posts})