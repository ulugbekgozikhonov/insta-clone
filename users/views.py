from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginView(View):
	def get(self, request):
		return render(request, 'login.html')

	def post(self, request):
		data = request.POST
		username = data.get('username')
		password = data.get('password')
		user = authenticate(request, username=username, password=password)
		if user:
			login(request, user)
			return redirect('post-list')
		return render(request, 'login.html',{"error": "username or password error"})

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    
    def post(self, request):
        data = request.POST
        email_or_phone = data.get('email_or_phone')
        full_name = data.get('full_name')
        username = data.get('username')
        password = data.get('password')
        
        if User.objects.filter(email=email_or_phone).exists():
            return render(request, 'register.html', {"error_email": "This email already is a taken"})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {"error_username": "This username already is a taken"})
        
        User.objects.create_user(
			email=email_or_phone,
			first_name=full_name,
			username=username,
			password=password
		)
        
        return redirect("login")

@login_required()
def logout_view(request):
    logout(request=request)
    return redirect('login')

class ProfileView(LoginRequiredMixin,View):
    def get(self,request, username):
        user = User.objects.get(username=username)
        return render(request,"profile.html", {"user": user})