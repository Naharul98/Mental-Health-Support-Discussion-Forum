from django.shortcuts import render
from django.http import Http404
from django.conf import settings
from django.views import View
from .models import Entry
from django.db.models import Count
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
# Create your views here.
class HomeView(View):
    def get(self, request):
        root_nodes = Entry.objects.root_nodes()
        root_nodes = root_nodes.annotate(overall_votes=(Count("upvotes") - Count("downvotes"))).order_by("-overall_votes")
        page = request.GET.get('page', 1)
        paginator = Paginator(root_nodes, 5)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        return render(request, "home.html", {"entries": queryset})

class HelpView(View):
    def get(self, request):
        return render(request, "help.html")


class HomeSort(View):
    def get(self, request, sorting):
        root_nodes = Entry.objects.root_nodes()
        if sorting=='new':
            root_nodes = root_nodes.annotate(overall_votes=(Count("upvotes") - Count("downvotes"))).order_by("-created_date")
        elif sorting == 'trending':
            root_nodes = root_nodes.annotate(overall_votes=(Count("upvotes") - Count("downvotes")), trending_score=Count("children")).order_by("-trending_score")
        page = request.GET.get('page', 1)
        paginator = Paginator(root_nodes, 5)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        return render(request, "home.html", {"entries": queryset})

class MyDiscussionsView(View):
    def get(self, request, username):
        root_nodes = Entry.objects.root_nodes()
        root_nodes = root_nodes.filter(user=request.user)
        root_nodes = root_nodes.annotate(overall_votes=(Count("upvotes") - Count("downvotes"))).order_by("-created_date")

        page = request.GET.get('page', 1)
        paginator = Paginator(root_nodes, 5)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        return render(request, "home.html", {"entries": queryset})

class CreatePost(View):
    def get(self, request):
        return render(request, "create_post.html")

    def post(self, request):
        entry = Entry(user=request.user, content=request.POST.get('post_detail', ""), title=request.POST.get('post_title', ""))
        entry.save()
        entry.upvotes.add(request.user)
        return redirect('posts-detail-view', pk_post=entry.id)

class DeletePost(View):
    def get(self, request, pk_post):
        Entry.objects.get(id=pk_post).delete()
        Entry.objects.rebuild()
        return redirect('home')

class ReplyPost(View):
    def get(self, request, pk_post):
        return render(request, "reply_post.html", {"entry": Entry.objects.get(pk=pk_post)})
    def post(self, request,pk_post):
        entry = Entry(user=request.user, content=request.POST.get('reply', ""), parent=Entry.objects.get(pk=pk_post))
        entry.save()
        entry.upvotes.add(request.user)
        return redirect('posts-detail-view', pk_post=entry.root_pk)


class PostsDetailView(View):
    def get(self, request, pk_post):
        subtree = Entry.objects.get(pk=pk_post)
        title = subtree.title
        root_nodes = subtree.get_descendants(include_self=True)
        root_nodes = root_nodes.annotate(overall_votes=(Count("upvotes") - Count("downvotes")))
        return render(request, "post_detail.html", {"entries": root_nodes, "title" : title, "root_post_id" : pk_post, "is_parent": (subtree.parent == None)})

@csrf_exempt
def upvote(request):
    entry = Entry.objects.get(id=request.POST.get('pk_post'))
    data = {}
    data['id'] = entry.pk
    entry.downvotes.remove(request.user)
    if request.user in entry.upvotes.all():
        entry.upvotes.remove(request.user)
        data['user_upvoted'] = False
    else:
        entry.upvotes.add(request.user)
        data['user_upvoted'] = True

    data['upvotes'] = entry.upvotes.count()
    data['downvotes'] = entry.downvotes.count()

    x = json.dumps(data)
    return HttpResponse(x, content_type="application/json")

@csrf_exempt
def downvote(request):
    entry = Entry.objects.get(id=request.POST.get('pk_post'))
    data = {}
    data['id'] = entry.pk
    entry.upvotes.remove(request.user)
    if request.user in entry.downvotes.all():
        entry.downvotes.remove(request.user)
        data['user_downvoted'] = False
    else:
        entry.downvotes.add(request.user)
        data['user_downvoted'] = True

    data['upvotes'] = entry.upvotes.count()
    data['downvotes'] = entry.downvotes.count()

    x = json.dumps(data)
    return HttpResponse(x, content_type="application/json")