from django import forms
from blog.models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):
    """our post html form"""

    class Meta:
        model = Post
        fields = ('title', 'text','image' )

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text', )

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True, help_text='Optional')
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=True, help_text='Please Input a valid email account')
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']


        if commit:
            user.save()

        return user



