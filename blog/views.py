from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from requests import HTTPError

from .models import Post
from users.models import Profile
from .forms import CreatePost
from main import get_image_url


def home(request):
    posts = Post.objects.all().order_by('-date_posted')

    return render(request, 'blog/home.html', {'title': "Home", 'posts': posts})


@login_required(login_url='login')
def posts_list(request):
    user = request.user
    posts = user.post_set.all()
    return render(request, 'blog/post_list.html', {'title': "My Posts", 'posts': posts})


@login_required(login_url='login')
def add_post(request):
    if request.method == 'POST':
        form = CreatePost(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            tag = form.cleaned_data['tag']
            try:
                new_post.image_url = get_image_url(tag)
            except HTTPError:
                print("Couldn't get image from API")

            new_post.save()
            form.save_m2m()
            return redirect('blog-home')
    else:
        form = CreatePost()
    return render(request, 'blog/add_post.html', {'title': "Create Post", 'form': form})


def view_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(username=post.author)
    profile = Profile.objects.get(user=user)
    return render(request, 'blog/view_post.html', {'title': "Post", 'post': post, 'profile': profile})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'subtitle', 'content']

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
