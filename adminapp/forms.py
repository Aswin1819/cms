from django import forms
from blogs.models import BlogPost
from ckeditor.widgets import CKEditorWidget
from cloudinary.forms import CloudinaryFileField


class PostForm(forms.ModelForm):
    featured_image = CloudinaryFileField(
        required=False,
        options={
            'tags': 'blog_post',
            'format': 'jpg',
            'crop': 'limit',
            'width': 1200,
            'height': 800,
        }
    )
    
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'featured_image', 'attachements', 'status', 'featured']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title...'
            }),
            'content': CKEditorWidget(),
            'attachements': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['featured_image'].help_text = 'Upload an image for your blog post'
        self.fields['title'].help_text = 'Choose a catchy title for your post'