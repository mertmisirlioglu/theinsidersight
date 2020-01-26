from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile, Post


class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    GENDER = (
        ('E', 'Erkek'),
        ('K', 'Kadın'),
    )

    gender = forms.ChoiceField(choices=GENDER, label='', initial='',
                               widget=forms.Select(), required=True)

    FACULTY = (
        ('Mühendislik', 'Mühendislik'),
        ('Mimarlık', 'Mimarlık'),
        ('Fen-Edebiyat', 'Fen-Edebiyat'),
        ('İktisadi-İdari', 'İktisadi-İdari'),
        ('Güzel Sanatlar', 'Güzel Sanatlar')
    )

    faculty = forms.ChoiceField(choices=FACULTY, label='', initial='',
                                widget=forms.Select(), required=True)

    birthdate = forms.DateTimeField()

    class Meta:
        model = UserProfile
        fields = (
            'gender',
            'faculty',
            'birthdate',
            'user'
        )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {
            'content',
            'category'
        }


class ReplyPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {
            'content',
        }
