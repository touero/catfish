from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

class LoginView(View):
    template_name = 'login.html'  # 👈 添加这行

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['last_username'] = username
            return redirect('list_files')
        else:
            last_username = request.session.get('last_username', '')
            return render(request, 'login.html', {'last_username': last_username})