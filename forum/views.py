from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView  )
from forum.models import Post, Comment, Report
from forum.forms import PostForm, CommentForm,ReportForm
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from forum.filters import PostFilter
from news.models import News
from django.db.models import Count
# Create your views here.

class PostListView(ListView):
    model = Post
    #queryset = Post.objects.all()
    #context_object_name = 'posts' #more freindly template contexts
    template_name = "forum/post_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        context['myFilter'] = PostFilter(self.request.GET,queryset = Post.objects.all())
        context['posts'] = PostFilter(self.request.GET,queryset = Post.objects.all()).qs #.qs queryset to access filtered objs in view
        context['news'] = News.objects.filter(status=1).order_by('-published_date')[0:4]
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "forum/post_detail.html"

    #view count - mutiple views can be register for single user
    def get_object(self):
        obj = super().get_object()
        obj.view_count +=1
        obj.save()
        return obj

    form_class = CommentForm

    def post(self, request, pk, slug):
        post = get_object_or_404(Post, pk=pk, slug=slug)
        if request.method=="POST":
            form = self.form_class(request.POST or None)
            if form.is_valid():
                reply_id = int(request.POST.get('comment_pk'))
                text = request.POST.get('id_message')
                comment_qs = None
                if reply_id:
                    comment_qs = Comment.objects.get(pk=reply_id)
                comment = Comment.objects.create(post=post,user=request.user, text=text , reply= comment_qs)
                comment.save()
                return redirect('forum:post_detail', pk=post.pk, slug=post.slug)
        else:
            form = CommentForm()
        return render(request, self.template_name, {'form':form})

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')

        self.post = get_object_or_404(Post, pk=pk, slug=slug)

        # Add in a QuerySet of all the comment -- filtering reply attribut out (Self = None)
        context['comments'] = Comment.objects.filter(post=self.post, reply=None)
        context['news'] = News.objects.filter(status=1).order_by('-published_date')[0:3]
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'forum/post_edit.html'

    def post(self, request, *args, **kwargs):

        if request.method =='POST':
             #if this is a POST request in class-based views
            form = self.form_class(request.POST, request.FILES) #create form instance and populate with data

            if form.is_valid():
                post = form.save(commit=False) #commit False means do not save post yet as we need to add post author & created_date.
                post.author = request.user
                post.created_date = timezone.now()
                post.save()
                return redirect('forum:post_list')
        else:
            form = PostForm()
        return render(request, self.template_name, {'form': form})

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'forum/post_edit.html' #file for post location that requires udapting

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # UserPassesTestMixin - prevent user accessing other users post
    def test_func(self):
        post= self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'forum/post_confirm_delete.html'
    success_url = reverse_lazy('forum:post_list')

    # UserPassesTestMixin - prevent user accessing other users post
    def test_func(self):
        post= self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CreateCommentView(LoginRequiredMixin, CreateView):
    template_name = 'forum/add_comment_to_post.html'
    form_class = CommentForm

    def post(self, request, pk, slug):
        post =get_object_or_404(Post, pk=pk, slug=slug)
        if request.method=="POST":
            form = self.form_class(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()
                return redirect('forum:post_detail', pk=post.pk, slug=post.slug)
        else:
            form = CommentForm()
        return render(request, self.template_name, {'form':form} )

class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk= self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, pk=pk, slug=slug)
        url_ = post.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in post.likes.all():
                post.likes.remove(user)
            else:
                post.likes.add(user)
        return url_

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

class PostLikeAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None,slug=None, format=None):
        #pk= self.kwargs.get('pk')
        #slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, pk=pk, slug=slug)
        url_ = post.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if user in post.likes.all():
                liked = False
                post.likes.remove(user)
            else:
                liked = True
                post.likes.add(user)
            updated = True
        data ={
        "updated": updated,
        "liked" : liked,
        }
        return Response(data)



class ReportView(LoginRequiredMixin,CreateView):
    template_name = 'forum/report.html'
    form_class = ReportForm


    def post(self, request, pk, slug=None):
        comment =get_object_or_404(Comment, pk=pk)
        if request.method=="POST":
            form = self.form_class(request.POST or None)
            if form.is_valid():
                report = form.save(commit=False)
                report.user = request.user
                report.comment = comment
                report.save()
                return redirect('forum:post_detail', pk=comment.post.pk, slug=comment.post.slug)
        else:
            form = ReportForm()

        return render(request, self.template_name, {'form':form })

class GuidelinesView(TemplateView):
    template_name = 'forum/guidelines.html'


#function based
def trending(request):
    posts =Post.objects.filter(view_count__gte=50).order_by('-created_date')
    myFilter = PostFilter(request.GET,queryset =posts)
    posts = PostFilter(request.GET,queryset = posts).qs
    news = News.objects.filter(status=1).order_by('-published_date')[0:4]

    context ={
    'posts': posts,
    'myFilter': myFilter,
    'news': news,
    }
    return render(request,'forum/post_list.html', context )

def mostcomment(request):
    #created comment_count attribute in Post and counted comments
    posts = Post.objects.annotate(comment_count=Count('comments')).filter(comment_count__gte=10).order_by('-created_date')
    myFilter = PostFilter(request.GET,queryset =posts)
    posts = PostFilter(request.GET,queryset = posts).qs
    news = News.objects.filter(status=1).order_by('-published_date')[0:4]

    context ={
    'posts': posts,
    'myFilter': myFilter,
    'news': news,
    }
    return render(request,'forum/post_list.html', context )
