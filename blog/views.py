from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Post
from blog.forms import post_creation_form, post_header_removal_form

from django.core.paginator import Paginator
from django.db.models import Q

from django.template.defaultfilters import slugify
from datetime import datetime

from django.urls import reverse


def index(request):
    objects = Post.objects.values('author__username', 'author__userdetail__name', 'title', 'slug', 'posted_date', 'tags').order_by('-posted_date')

    query = request.GET.get('q')
    
    if query:
        objects = objects.filter(Q(author__username__icontains=query) | Q(author__userdetail__name__icontains=query) | Q(title__icontains=query) | Q(tags__icontains=query)).distinct()

    paginator = Paginator(objects, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'query': query}

    if query:
        return render(request, 'blog/search_post.html', context)
        
    return render(request, 'blog/index.html', context)


def category(request, category=None):
    objects = Post.objects.filter(tags__icontains=category).order_by('-posted_date')
    featured_post = objects.filter(featured_status=True)

    paginator = Paginator(objects, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'featured_post': featured_post, 'category': category}

    return render(request, 'blog/category.html', context)


def blog_post(request, slug=None):
    blog_post = get_object_or_404(Post, slug__exact=slug)
    related_post = Post.objects.filter(Q(tags__icontains=str(blog_post.tags[0]))).exclude(id=int(blog_post.pk)).order_by('-posted_date')[:5]

    context = {'blog_post': blog_post, 'related_post': related_post}

    return render(request, 'blog/blog_post.html', context)


def dashboard(request):
    if request.user.is_authenticated and request.user.userconfig.blog:

        user_blog_post = Post.objects.filter(author__username__exact=request.user.username).order_by('-posted_date')
        user_blog_post_count = user_blog_post.count()

        paginator = Paginator(user_blog_post, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'page_obj': page_obj, 'user_blog_post_count': user_blog_post_count}

        return render(request, 'blog/dashboard.html', context)

    return redirect('blog-index')


def create_post(request):
    if request.user.is_authenticated and request.user.userconfig.blog:

        form = post_creation_form(request.POST or None, request.FILES or None)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.slug = datetime.now().strftime('%d-%m-%Y-%I-%M-%S') + '-' + slugify(instance.title)

            instance.save()

            return redirect('blog-dashboard')

        return render(request, 'blog/create_post.html', {'form': form})

    return redirect('blog-index')


def edit_post(request, slug=None):
    if request.user.is_authenticated and request.user.userconfig.blog:

        user_blog_post = get_object_or_404(Post, slug__exact=slug)

        form = post_creation_form(request.POST or None, request.FILES or None, instance=user_blog_post)
        form_RH = post_header_removal_form(request.POST or None)
            
        if form.is_valid() and form_RH.is_valid():
            instance = form.save(commit=False)
            instance.slug = datetime.now().strftime('%d-%m-%Y-%I-%M-%S') + '-' + slugify(instance.title)

            if form_RH.cleaned_data['remove_header']:
                instance.header = None

            instance.save()

            return redirect('blog-dashboard')

        return render(request, 'blog/edit_post.html', {'form': form, 'form_RH': form_RH, 'user_blog_post': user_blog_post})

    return redirect('blog-index')


def delete_post(request, pk=None):
    if request.user.is_authenticated and request.user.userconfig.blog:

        user_blog_post = get_object_or_404(Post, id=pk)

        if request.user.id == user_blog_post.author.id:
            user_blog_post.delete()

        return redirect("blog-dashboard")

    return redirect('blog-index')
