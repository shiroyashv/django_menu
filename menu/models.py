from django.db import models
from django.utils.translation import gettext_lazy as _


class Menu(models.Model):
    name = models.CharField(_('name'), max_length=50)

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(_('name'), max_length=50)
    url = models.CharField(_('URL'), max_length=200, blank=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_('parent'), related_name='children'
        )
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, verbose_name=_('Menu'),
        related_name='items'
        )

    class Meta:
        verbose_name = _('Menu Item')
        verbose_name_plural = _('Menu Items')

    def __str__(self):
        return self.name

    def is_active(self, request):
        if self.url:
            return request.path == self.url
        return False

    def is_dropdown(self):
        return self.children.exists()
