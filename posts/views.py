from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .models import Post, PostLike, Comment
from .forms import CommentForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json

class PostListView(LoginRequiredMixin, View):
    def get(self, request):
        comment_form = CommentForm()
        user = request.user

        # Foydalanuvchining all likes
        user_liked_post_ids = set(
            PostLike.objects.filter(user=user, deleted=False).values_list("post_id", flat=True)
        )

        # Postlar (faqat boshqa userlar tomonidan yaratilganlar)
        posts = Post.objects.exclude(user=user).all()

        # Har bir postga liked atributini qo‘shamiz
        for post in posts:
            post.liked = post.id in user_liked_post_ids

        return render(request, "index.html", {
            "posts": posts,
            "comment_form": comment_form
        })


class PostCommentView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        data = json.loads(request.body)
        text = data.get('text')

        comment = Comment.objects.create(
            post=post,
            user=request.user,
            text=text
        )

        return JsonResponse({
            'id': comment.id,
            'username': request.user.username,
            'text': comment.text
        })


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
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        post_like = post.likes.filter(post=post, user=request.user).first()

        if post_like:
            post_like.deleted = not post_like.deleted
            post_like.save()
            liked = not post_like.deleted
        else:
            post.likes.create(user=request.user)
            liked = True

        likes_count = post.likes.filter(deleted=False).count()

        return JsonResponse({'liked': liked, 'likes_count': likes_count})
