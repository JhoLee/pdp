from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View, FormView

from .forms import PostForm
from .models import Post
from .tasks import sleepy
from .utils import encrypt, check_pw, get_alert, set_alert
from front.celery import debug_task


def index(req, **kwargs):
    return render(req, 'mask/index.html')


class IndexView(ListView):
    template_name = 'mask/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.order_by('-reg_date')[:5]


class PostDetailView(View):

    def get(self, req, pk):
        context = {}
        try:
            post = Post.objects.get(pk=pk)
            context['post'] = post
            set_alert(req, "이미지를 보려면, 암호를 입력하셔야 합니다.", type="INFO")
            return render(req, 'mask/check_password.html', context)
        except Exception:
            set_alert(req, "The post was not found.", "ERROR", type="DANGER")
            context['posts'] = Post.objects.order_by('-reg_date')

            return render(req, 'mask/index.html', context)

    def post(self, req, pk):
        context = {}

        try:
            if 'password' not in req.POST.keys():
                set_alert(req, "Error", "ERROR", "DANGER")

            input_pw = req.POST['password']
            post = Post.objects.get(pk=pk)
            context['post'] = post
            hashed_pw = post.password
            if check_pw(input_pw, hashed_pw):
                # context['alert'] = get_alert("Password match!", type="SUCCESS")
                if post.status == Post.Status.STAND_BY:
                    set_alert(req, "작업 대기중입니다.", type="NORMAL")
                else:
                    set_alert(req, title="작업 완료!", msg="아래 다운로드 버튼을 눌러보세요!", type="SUCCESS")

                return render(req, 'mask/detail.html', context)
            else:
                set_alert(req, "비밀번호가 틀립니다.", type="DANGER")

                return render(req, 'mask/check_password.html', context)
        except Exception:
            set_alert(req, "The post was not found.", type="WARN")
            return render(req, 'mask/index.html', context)


class _PostDetailView(DetailView):
    model = Post
    template_name = 'mask/detail.html'


class PostFormView(FormView):
    def get(self, request, **kwargs):
        form = PostForm()
        context = {'form': form}
        return render(request, 'mask/post.html', context=context)

    def post(self, request, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            #
            post.password = encrypt(post.password)
            post.save()
            pk = post.pk
            return redirect('mask:detail', pk=pk)


class PostDeleteView(View):
    def get(self, req, pk):
        context = {}
        try:
            post = Post.objects.get(pk=pk)
            context['post'] = post
            set_alert(req, "이미지를 삭제하려면, 암호를 입력하셔야 합니다.", type="INFO")
            return render(req, 'mask/check_password.html', context)
        except Exception:
            set_alert(req, "The post was not found.", "ERROR", type="DANGER")
            context['posts'] = Post.objects.order_by('-reg_date')

            return render(req, 'mask/index.html', context)

    def post(self, req, pk):
        context = {}

        try:
            if 'password' not in req.POST.keys():
                set_alert(req, "Error", type="DANGER")
            input_pw = req.POST['password']
            post = Post.objects.get(pk=pk)
            context['post'] = post
            hashed_pw = post.password
            if check_pw(input_pw, hashed_pw):
                post.delete()
                set_alert(req, "삭제되었습니다.", type="SUCCESS")

                return render(req, 'mask/index.html', context)
            else:
                set_alert(req, "비밀번호가 틀립니다.", type="DANGER")

                return render(req, 'mask/check_password.html', context)
        except Exception:
            set_alert(req, "The post was not found.", type="WARN")
            return render(req, 'mask/index.html', context)
