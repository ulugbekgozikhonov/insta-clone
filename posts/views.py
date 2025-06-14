from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .models import Post, Comment
from .forms import CommentForm


class PostListView(LoginRequiredMixin, View):
    def get(self, request):
        posts = Post.objects.exclude(user=request.user).all()
        comment_form = CommentForm()
        return render(
            request, "index.html", {"posts": posts, "comment_form": comment_form}
        )

    def post(self, request):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            post_id = request.POST.get("post_id")
            post = Post.objects.get(id=post_id)
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))


class AddpostView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "add_post.html")

    def post(self, request):
        data = request.POST
        title = data.get("title")
        description = data.get("description")
        file = request.FILES.get("file")
        try:
            Post.objects.create(
                title=title, description=description, content=file, user=request.user
            )
        except Exception as e:
            return render(request, "add_post.html", {"error": e})

        return redirect("post-list")


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        post_like = post.likes.filter(post=post, user=request.user).first()
        if post_like:
            post_like.deleted = not post_like.deleted
            post_like.save()
        else:
            post.likes.create(user=request.user)

        return redirect(request.META.get('HTTP_REFERER', '/'))
