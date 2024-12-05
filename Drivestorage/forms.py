from django import forms
from .models import Folder, File, FileRoot

# Form for creating/editing folders
class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'description']

    name = forms.CharField(max_length=255, label='Folder Name', widget=forms.TextInput(attrs={'placeholder': 'Enter folder name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter folder description'}), required=False)

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file']

    name = forms.CharField(max_length=255, label='File Name', widget=forms.TextInput(attrs={'placeholder': 'Enter file name'}))
    file = forms.FileField(label='Choose a file')

class FileRootForm(forms.ModelForm):
    class Meta:
        model = FileRoot
        fields = ['name', 'file']

    name = forms.CharField(max_length=255, label='File Name', widget=forms.TextInput(attrs={'placeholder': 'Enter file name'}))
    file = forms.FileField(label='Choose a file')
