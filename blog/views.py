from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from blog.models import Post, Comment
from django.utils import timezone
from blog.forms import PostForm , CommentForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView, DetailView, UpdateView, CreateView, DeleteView,
)
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

def post_list(request):
    """show post list"""
    template_name = 'blog/post_list.html'
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context = {'posts': posts,}
    return render(request, template_name, context)

def post_detail(request, pk):
    """show detail"""
    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, pk=pk)
    context = {'post':post}
    return render(request, template_name, context)

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)#save but do not commit to the database yet until user has been confirmed
            # print("before, ", post)
            post.author = request.user
            #post.published_date = timezone.now()
            # print("after, ", post)
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    template_name = 'blog/post_edit.html'
    context = {'form': form,}
    return render(request, template_name, context)

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    template_name = 'blog/post_edit.html'
    context = {'form':form}
    return render(request, template_name, context)

@login_required
def post_remove(request, pk):
    post = Post.objects.get(pk=pk).delete()
    return redirect('blog:post_list')

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    template_name = 'blog/post_draft_list.html'
    context = {'posts':posts}
    return render(request, template_name, context)

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect(post.get_absolute_url())#redirects to the post_detail page defined as a fxn (get_absolue_url) in models.py 

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
        template_name = 'blog/add_comment_to_post.html'
        context = {'form':form}
    return render(request, template_name, context)

def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)
    
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog:post_detail', pk=comment.post.pk)

# def signup(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # username = user.cleaned_data.get('username')
#             # raw_password = user.cleaned_data.get('password1')
#             # user = authenticate(username=username, password=raw_password)
#             # login(request, user)
#             return redirect('blog:post_list')
#     else:
#         form = RegisterForm()
#         context = {'form': form}
#         template_name = 'registration/signup.html'
#     return render(request, template_name, context)

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:post_list')
    else:
        form = RegisterForm()
        
        template_name = 'registration/signup.html'
        
        context = {'form': form}
    return render(request, template_name, context)


def search(request):
    template_name = 'blog/post_list.html'
    if request.method == 'GET':
        search_data = request.GET.get('q')
        # print(search_data)
        results = Post.objects.filter(title__icontains=search_data)
        context = {'posts': results, 'search':True}
        return render(request, template_name, context)
    else:
        # context = {'posts': None}
        return redirect("blog:post_list")





#CLASS BASED VIEW. in class based view all we need to specify is the model and the template.
class PostList(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_edit.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        # form.instance.image = form.cleaned_data['image']
        form.save()
        return super(PostCreate, self).form_valid(form)#super helps to take all of the properties of the form_valid fxn into the postcreate class

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_edit.html'
    form_class = PostForm

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:post_list')













