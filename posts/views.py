from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .models import Post

class PostListView(LoginRequiredMixin, View):
    def get(self, request):
        posts = Post.objects.exclude(user=request.user).all()
        return render(request, "index.html", {"posts": posts})

 
class AddpostView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,"add_post.html")

    def post(self, request):
        data = request.POST
        title = data.get('title')
        description = data.get('description')
        file = request.FILES.get('file')
        try:
            Post.objects.create(
                title=title,
                description=description,
                content=file,
                user=request.user
            )
        except Exception as e:
            return render(request, 'add_post.html', {"error": e})
        
        return redirect('post-list')