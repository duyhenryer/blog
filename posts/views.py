from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from urllib.parse import quote_plus
from django.db.models import Q
from .models import Post
from .forms import PostForm
from comments.forms import CommentForm
from comments.models import Comment
from django.utils import timezone



def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        #messages success
        return render(request, "post_list.html")
        # messages.success(request,"scusses ")
        # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
            "form": form,
    }
    return render(request, "post_form.html", context)

def post_detail(request,slug=None):

    instance = get_object_or_404(Post, slug=slug)
    share_string = quote_plus(instance.content)
    initial_data = {
            "content_type": instance.get_content_type,
            "object_id": instance.id,
        }

    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():

        # new_comment = form.save(commit=False)
        # new_comment.post = Post
        # new_comment.save()

        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        # new_comment, created = Comment.objects.get_or_create(
        #     user=request.user,
        #     content_type=content_type,
        #     object_id=obj_id,
        #     content=content_data,
        # )

        content = {
            "content_type": content_type,
            "obj_id": obj_id,
            "content_data": content_data,
        }

        # return HttpResponseRedirect(content_object.get_absolute_url())
        return render(request, content)
    # comments = instance.comments


    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "comment_form": form,
    }


    return render(request, "post_detail.html", context)


#
# def post_detail(request,slug=None):
#     instance = get_object_or_404(Post, slug=slug)
#     share_string = quote_plus(instance.content)
#     # content_type = ContentType.objects.ge
# t_for_model(Post)
#     # obj_id = instance.id
#     comments = Comment.objects.filter_by_instance(instance)
#
#     initial_data = {
#             "content_type": instance.get_content_type,
#             "object_id": instance.id,
#         }
#     form = CommentForm(request.POST or None, initial=initial_data)
#     if form.is_valid():
#         print(form.cleaned_data)
#
#         c_type = form.cleaned_data.get("content_type")
#         content_type = ContentType.objects.get(model=c_type)
#         obj_id = form.cleaned_data.get("object_id")
#         content_data = form.cleaned_data.get("content")
#         new_comment, created = Comment.objects.get_or_create(
#             user=request.user,
#             content_type=content_type,
#             object_id=obj_id,
#             content=content_data,
#         )
#         #
#         # if created:
#         #     print("Yeeeee....")
#
#     comments = instance.comments
#     context = {
#         "title": instance.title,
#         "instance": instance,
#         "share_string": share_string,
#         "comments": comments,
#         "comment_form": form,
#
#     }
#
#     return render(request, "post_detail.html", context)
#
#

def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.all()  #.all()  #.order_by("-timestamp")

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(Q(title__icontains=query)
                                             | Q(content__icontains=query)
                                             | Q(user__first_name__icontains=query)
                                             | Q(user__last_name__icontains=query)).distinct()
    paginator = Paginator(queryset_list, 10)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    content = {
        "object_list": queryset,
        # "title": "ExplorePic",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "post_list.html", content)


def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>item</a> saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    content = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }

    return render(request,"post_form.html", content)

def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "successfully delete")
    return redirect("posts:list")



