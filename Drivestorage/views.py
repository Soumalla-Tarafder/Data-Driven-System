from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from Drive.forms import UserRegistrationForm, UserLoginForm
from .forms import FolderForm,FileForm,FileRootForm
from .models import Folder,File,FileRoot
from django.contrib.auth.decorators import login_required


def register(request):

    if request.method == "POST":
        name = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        print("sadsad")
        if User.objects.filter(username=name).exists():
            return render(request,'register.html')
        user = User.objects.create_user(username = name,
                                        email = email,
                                        password=password)
        user.save()
                    
        return redirect('login')

    else:
        return render(request,'register.html')
    
    return render(request,'register.html')


def user_login(request):

    if request.method== "POST":
        username = request.POST['username']
        password = request.POST['password']


        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('dashboard')
        else:
            return redirect("login")
    return render(request,'login.html')

def create_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.owner = request.user
            folder.save()
            return redirect('folder_detail', folder_id=folder.id) 
    else:
        form = FolderForm()

    return render(request, 'create_folder.html', {'form': form})

def create_file(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.owner = request.user
            file.folder = folder
            file.save()
            return redirect('folder_detail', folder_id=folder.id)
    else:
        form = FileForm()
    return render(request, 'create_file.html', {'form': form, 'folder': folder})

@login_required
def dashboard(request):
    folders = Folder.objects.filter(owner=request.user, parent__isnull=True)

    files = FileRoot.objects.filter(owner=request.user)
    
    return render(request, 'dashboard.html', {'folders': folders, 'files': files})

def user_logout(request):
    logout(request)
    return redirect('login') 


@login_required
def folder_detail(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
    print(folder,folder_id)
    subfolders = Folder.objects.filter(parent=folder)
    files = File.objects.filter(folder=folder)

    return render(request, 'folder_detail.html', {
        'folder': folder,
        'subfolders': subfolders,
        'files': files
    })

@login_required
def upload_file(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    print(folder)
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.owner = request.user
            file.folder = folder
            file.save()
            return redirect('folder_detail', folder_id=folder.id)
    else:
        form = FileForm()
    
    return render(request, 'upload_file.html', {'form': form, 'folder': folder})

@login_required
def upload_file_root(request):

    if request.method == 'POST':
        form = FileRootForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            print(file)
            file.owner = request.user
            file.save()
            return redirect('dashboard')
    else:
        form = FileRootForm()
    
    return render(request, 'upload_files_root.html', {'form': form})

def delete_root_file(request, fileid):
    print(fileid)
    fileroot = get_object_or_404(FileRoot, id=fileid)
    print(fileroot)
    # Check if the user is the owner of the folder
    if fileroot.owner == request.user:
        fileroot.delete()  # Delete the folder
        return redirect('dashboard')  # Redirect to the dashboard after deletion
    else:
        # Optionally handle permission issues
        return redirect('dashboard')
    
def delete_folder(request, folder_id):

    folder = get_object_or_404(Folder, id=folder_id)
    
    # Check if the user is the owner of the folder
    if folder.owner == request.user:
        folder.delete()  # Delete the folder
        return redirect('dashboard')  # Redirect to the dashboard after deletion
    else:
        # Optionally handle permission issues
        return redirect('dashboard')
    

def create_subfolder(request, folder_id):
    parent_folder = get_object_or_404(Folder, id=folder_id)

    # Check if the logged-in user is the owner of the parent folder
    if parent_folder.owner != request.user:
        raise Http404("You do not have permission to create a subfolder in this folder.")

    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            subfolder = form.save(commit=False)
            subfolder.parent = parent_folder
            subfolder.owner = request.user 
            subfolder.save()
            return redirect('folder_detail', folder_id=parent_folder.id)
    else:
        form = FolderForm()

    return render(request, 'create_subfolder.html', {'form': form, 'folder': parent_folder})


@login_required
def delete_file(request, file_id):
    # Retrieve the file to delete
    file = get_object_or_404(File, id=file_id)

    # Ensure the file belongs to the logged-in user's folder (optional security check)
    if file.folder.owner != request.user:
        raise Http404("You do not have permission to delete this file.")

    # Delete the file
    file.delete()

    # Redirect to the folder detail page
    return redirect('folder_detail', folder_id=file.folder.id)