from django import template

register = template.Library()

@register.filter
def get_field_verbose_name(fields_dict, field_name):
    """
    Retorna o verbose_name de um campo específico.
    Uso: {{ form.fields|get_field_verbose_name:field_name }}
    """
    if field_name in fields_dict:
        return fields_dict[field_name].label or field_name.replace('_', ' ').capitalize()
    return field_name.replace('_', ' ').capitalize() 