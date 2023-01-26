from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    url = models.CharField(max_length=200, blank=True)

    @classmethod
    def get_menu(cls, menu_name):
        return cls.objects.filter(name=menu_name)
