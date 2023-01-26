import re
from django import template
from django.urls import reverse

from ..models import Menu


register = template.Library()

@register.simple_tag
def draw_menu(menu_name, request):
    try:
        menu = Menu.get_menu(menu_name)
        current_url = request.path
        active_menu = None
        for item in menu:
            if item.url == current_url:
                active_menu = item
                break
        return render_menu(menu, active_menu)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(e)

        return ''


def render_menu(menu_items, active_url):
    html = '<ul>'
    for item in menu_items:
        li = '<li '
        if item.url == active_url:
            li = add_class(li, 'expanded')
            li = add_class(li, 'active')
            li += '<a href="%s">%s</a>' % (item.url, item.name)
            li += render_children(item.children.all(), active_url)
            li = add_class(li, 'expanded')
        else:
            li += '>'
            li += '<a href="%s">%s</a>' % (item.url, item.name)
            li += render_children(item.children.all(), active_url)
        li += '</li>'
        html += li
    html += '</ul>'
    return html

def render_children(children, active_url):
    html = ""
    for child in children:
        li = '<li '
        if child.url == active_url:
            li = add_class(li, 'expanded')
            li = add_class(li, 'active')
            li += '<a href="%s">%s</a>' % (child.url, child.name)
            li += render_children(child.children.all(), active_url)
            li = add_class(li, 'expanded')
        else:
            li += '>'
            li += '<a href="%s">%s</a>' % (child.url, child.name)
            li += render_children(child.children.all(), active_url)
        li += '</li>'
        html += li
    return html

def add_class(li, class_name):
    class_attr = 'class="%s"' % class_name
    if 'class=' in li:
        li = re.sub(r'class="([^"]+)"', r'class="\1 %s"' % class_name, li)
    else:
        li = li.replace('>', ' %s>' % class_attr)
    return li
