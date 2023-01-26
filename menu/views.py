from django.shortcuts import render


def menu(request):
    return render(request, 'template.html', {'menu_name': 'main_menu', 'request': request})
