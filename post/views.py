from django.shortcuts import render

from .models import (
    Category,
    Contact,
    Post,
    SubCategory,
)

from comment.models import Comment


def post_manipulate(no):

    posts = []
    counter = 0
    for post in Post.objects.all():
        if counter != no:
            print(post.title)
            posts.append(post)
        else:
            break
        counter += 1

    # most_view = [first_sub.last(), second_sub.last()]
    return posts


def most_viewed(no):

    posts = Post.objects.all().order_by('-views')

    return posts[:no]


def most_read_in_cat(no, posts):
    length = len(posts)
    # posts = Post.objects.all()
    modified_posts = posts[1:]

    return modified_posts[:no+1]


def index(request):
    template_name = "./post/index.html"
    most_view_posts = Post.objects.filter(lead=True).order_by("-pk")
    most_view = most_view_posts[:2]
    mostRead = most_viewed(4)
    posts = Post.objects.all().order_by('-pk')
    recent = posts[:3]
    context = {'mostRead': most_view,
               'recent': recent,
               'most_read': mostRead,
               'categories': Category.objects.all(),
               'featured_posts': Post.objects.filter(featured=True).order_by("-pk")}
    return render(request, template_name, context)


def read(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.views += 1
    post.save()
    most_read = most_viewed(4)
    template_name = "./post/read.html"
    comments = Comment.objects.filter(post=post, parent=None)
    if request.method == "POST":
        if request.POST.get('parent'):
            parent = Comment.objects.get(pk=int(request.POST.get('parent')))
            message = request.POST.get('message')
            comment = Comment(user=request.user, post=post, content=message, parent=parent)
            comment.save()
        else:
            message = request.POST.get('message')
            comment = Comment(user=request.user, post=post, content=message)
            comment.save()

    context = {'post': post,
               'mostRead': most_read,
               'featured_posts': Post.objects.filter(featured=True).order_by("-pk"),
               'catsIn': Category.objects.all(),
               'comments': comments,
               }
    return render(request, template_name, context)

# class Read(generic.TemplateView):jm
#     template_name = ""


def editComment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if request.method == "POST":
        if request.user == comment.user:
            message = request.POST.get("message")
            comment.content = message
            comment.save()
    return render(request, './post/editComment.html', {'comment': comment})

def removeComment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if request.method == "POST":
        if request.user == comment.user:
            comment.delete()
    return render(request, './post/deleteComment.html', {'comment': comment})



def sub_category(request, sub_id):
    sub_cat = SubCategory.objects.get(pk=sub_id)
    most_view = most_viewed(4)
    postsIn = sub_cat.post_set.all().order_by('-pk')
    first = postsIn.first()
    try:
        two_post = [postsIn[1], postsIn[2]]
    except:
        if len(postsIn) >= 2:
            two_post = [postsIn[1]]
        else:
            two_post = []
    if len(postsIn) > 3:
        posts = postsIn[3:]
    else:
        posts = []
    # for post in postsIn[1:]:
    #     if post not in two_post:
    #         posts.append(post)

    template_name = "./post/sub_category.html"
    context = {'subCategory': sub_cat,
               'posts': posts,
               'first': first,
               'two_post': two_post,
               'most_view': most_view,
               'cats': Category.objects.all(),
               }
    return render(request, template_name, context)


def popular(request):
    postsIn = Post.objects.all().order_by('-views')
    first = postsIn.first()
    most_view = most_viewed(4)
    try:
        two_post = [postsIn[1], postsIn[2]]
    except:
        if len(postsIn) >= 2:
            two_post = [postsIn[1]]
        else:
            two_post = []

    if len(postsIn) > 3:
        posts = postsIn[3:11]
    else:
        posts = []
    template_name = "./post/popular.html"
    context = {
               'posts': posts,
               'first': first,
               'two_post': two_post,
               'most_view': most_view,
               'cats': Category.objects.all(),
               }
    return render(request, template_name, context)
# class CategoryIn(generic.TemplateView):
#     template_name = "./post/category.html"


def about_us(request):
    # sub_cats = SubCategory.objects.all()
    most_read = most_viewed(4)
    template_name = "./post/aboutUs.html"
    context = {'most_read': most_read}
    return render(request, template_name, context)


# class AboutUs(generic.TemplateView):
#     template_name = './post/aboutUs.html'


def contact(request):
    template_name = "./post/contact.html"
    if request.method == "POST":
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        con = Contact(email=email, subject=subject, message=message)
        con.save()
    return render(request, template_name)
