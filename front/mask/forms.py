from django.forms import ModelForm, forms, TextInput, PasswordInput, FileInput
from .models import Post

from django.utils.translation import gettext_lazy as _


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'author', 'password', 'image']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': "30자 이내로 입력 가능합니다."}),
            'author': TextInput(attrs={'class': 'form-control', 'placeholder': "10자 이내로 입력 가능합니다."}),
            'password': PasswordInput(
                attrs={'class': 'form-control', 'placeholder': "20자 이내로 입력해주세요.", 'required': 'true'}),
            'image': FileInput(attrs={'class': 'form-control-file', 'placeholder': "이미지 혹은 영상을 업로드해주세요."}),

        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['maxlength'] = 30
        self.fields['author'].widget.attrs['maxlength'] = 10
        self.fields['password'].widget.attrs['maxlength'] = 20
        self.fields['image'].required = True

    def save(self, commit=True):
        self.instance = Post(**self.cleaned_data)
        if commit:
            self.instance.save()
        return self.instance
