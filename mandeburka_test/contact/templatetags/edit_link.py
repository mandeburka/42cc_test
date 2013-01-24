from django import template
from django.db import models
from django.core import urlresolvers

register = template.Library()


@register.tag(name="edit_link")
def edit_link(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, value = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires exactly one arguments" %
            token.contents.split()[0])
    return EditLinkNode(value)
    return ''


class EditLinkNode(template.Node):
    def __init__(self, model_object):
        self.model_object = template.Variable(model_object)

    def render(self, context):
        try:
            actual_object = self.model_object.resolve(context)
            if isinstance(actual_object, models.Model):
                return '<a href="%s">%s</a>' % (
                    urlresolvers.reverse(
                    'admin:%s_%s_change' %
                    (
                        actual_object._meta.app_label,
                        str(actual_object.__class__.__name__).lower()),
                    args=(actual_object.id,)),
                    actual_object.__class__.__name__
                )
        except template.VariableDoesNotExist:
            pass
        return ''
