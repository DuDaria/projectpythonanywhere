from django import forms
from django.contrib.auth.models import User 
from .models import Post, Comment, Message


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = ['category', 'price', 'name_descript','description', 'image']

        labels = {
            'category':'Выберите категорию',
            'price': 'Укажите цену',
            'name_descript':'Заголовок поста',
            'description': 'Описание поста',
            'image':'Выберите файл',
        }

        widjets = {
            'category':forms.Textarea(attrs={
                'class': 'form__category', 
                'placeholder': 'Описание поста',
            }),
            'price':forms.Textarea(attrs={
                'class': 'form__textarea', 
                'placeholder': 'Цена',
            }),
            'name_descript':forms.Textarea(attrs={
                'class': 'form__title', 
                'placeholder': 'Название поста',
            }),
            'description':forms.Textarea(attrs={
                'class': 'form__text', 
                'placeholder': 'Описание поста',
            }),
            'image':forms.ClearableFileInput(attrs={
                'class': 'form__file', 
                'type': 'file',
            }),
        }


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment

        fields =['text']

        labels = {
            'text': 'Оставьте комментарий'
        }

        widjets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст комментария'
            })
        } 

class MessageForm(forms.ModelForm):
    
    class Meta:
        model = Message

        fields =['text']

        labels = {
            'text': 'Текст сообщения',
        }

        widjets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст сообщения'
            }),
        } 

