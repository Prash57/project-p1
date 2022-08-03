from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from .forms import PostForm, CreateUserForm, CommentForm, AddTagsForm, ImageForm
from .filters import PostFilter
from .decorators import unauthenticated_user, allowed_users

from django.views.generic import CreateView


from .models import Post, Comment, Tag, Image
# Create your views here.


@login_required(login_url="posts")  # posts, home
# @allowed_users(allowed_roles=['super admin'])
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('login')

    context = {'form': form}
    return render(request, 'base/register.html', context)


@login_required(login_url="posts")  # posts, home
def addtags(request):
    form = AddTagsForm()

    if request.method == 'POST':
        form = AddTagsForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('posts')

    context = {'form': form}
    return render(request, 'base/add_tags.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('posts')  # posts, home

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('posts')  # posts, home
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'base/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('posts')  # posts, home


def home(request):
    return render(request, 'base/posts.html')  # posts.html, index.html

# @method_decorator(login_required, name='dispatch')


class TagsCreateView(CreateView):
    #model = Tag
    #template_name = "base/add_tags.html"
    #fields = '__all__'

    def get_success_url(self):
        return reverse('posts')


def posts(request):
    posts = Post.objects.all().order_by('-id')
    myFilter = PostFilter(request.GET, queryset=posts)

    posts = myFilter.qs
    page = request.GET.get('page')

    paginator = Paginator(posts, 10)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, 'myFilter': myFilter}
    return render(request, 'base/posts.html', context)


def post(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comment.objects.filter(post=post).order_by('-id')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            body = request.POST.get('body')
            comment = Comment.objects.create(
                post=post, name=request.POST['name'], body=body)
            comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {'post': post, 'comments': comments,
               'comment_form': comment_form}
    return render(request, 'base/post.html', context)


def profile(request):
    return render(request, 'base/profile.html')


def contact(request):
    return render(request, 'base/contact.html')

# def services(request):
#     return render(request, 'base/services.html')


@login_required(login_url="home")
def addimage(request):
    img = Image.objects.all()
    form = ImageForm()

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('gallery')

    context = {'img': img, 'form': form}
    return render(request, 'base/add_image.html', context)


def gallery(request):
    img = Image.objects.all().order_by('-id')
    form = ImageForm()

    page = request.GET.get('page')

    paginator = Paginator(img, 30)

    try:
        img = paginator.page(page)
    except PageNotAnInteger:
        img = paginator.page(1)
    except EmptyPage:
        img = paginator.page(paginator.num_pages)

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('gallery')

    context = {'img': img, 'form': form}
    return render(request, 'base/gallery.html', context)


# CRUD VIEWS
@login_required(login_url="posts")  # posts, home
def createPost(request):
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('posts')

    context = {'form': form}
    return render(request, 'base/post_form.html', context)


@login_required(login_url="posts")  # posts, home
def updatePost(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('posts')

    context = {'form': form}
    return render(request, 'base/post_form.html', context)


@login_required(login_url="posts")  # posts, home
def deletePost(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        post.delete()
        return redirect('posts')
    context = {'item': post}
    return render(request, 'base/delete.html', context)


def sendEmail(request):

    if request.method == 'POST':

        template = render_to_string('base/email_template.html', {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'message': request.POST['message'],
        })

        email = EmailMessage(
            request.POST['subject'],
            template,
            settings.EMAIL_HOST_USER,
            ['aprashant057@gmail.com']
        )

        email.fail_silently = False
        email.send()

    return render(request, 'base/email_sent.html')
