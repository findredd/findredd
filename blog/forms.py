from django import forms

from blog.models import Post


class post_creation_form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "header", "content", "tags"]
        widgets = {
            'header': forms.FileInput,
        }


class post_header_removal_form(forms.Form):
    remove_header = forms.BooleanField(label='Remove header', required=False)
