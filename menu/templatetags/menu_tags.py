from django import template
from django.utils.safestring import mark_safe

from ..models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    menu_items = MenuItem.objects.filter(menu__name=menu_name)

    active_item = None
    for item in menu_items:
        if item.is_active(context['request']):
            active_item = item
            break

    menu_html = '<ul>'

    menu_dict = {}
    for item in menu_items:
        parent_id = item.parent_id
        if parent_id in menu_dict:
            menu_dict[parent_id].append(item)
        else:
            menu_dict[parent_id] = [item]

    def build_menu(item, menu_dict, active_item):
        menu_html = ''
        active_class = 'active' if active_item == item else ''
        dropdown_class = 'dropdown' if item.is_dropdown() else ''
        expanded_class = 'expanded' if active_item and (active_item == item or active_item.parent == item) else ''
        menu_html += f'<li class="{dropdown_class} {expanded_class}">'
        menu_html += f'<a class="{active_class}" href="{item.url}">{item.name}</a>'
        if item.id in menu_dict:
            menu_html += '<ul>'
            for child_item in menu_dict[item.id]:
                menu_html += build_menu(child_item, menu_dict, active_item)
            menu_html += '</ul>'
        menu_html += '</li>'
        return menu_html

    root_items = menu_dict.get(None, [])
    for item in root_items:
        menu_html += build_menu(item, menu_dict, active_item)

    menu_html += '</ul>'
    return mark_safe(menu_html)
