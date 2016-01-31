from django import template
from django.utils.translation import ugettext
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def volunteer_state(organisation, volunteer):
    def state_tag(state, label):
        if state == 'free':
            klass = 'info'
        elif state == 'accepted':
            klass = 'success'
        elif state == 'invited':
            klass = 'warning'
        else:
            klass = 'danger'
        return mark_safe('<span class="label label-' + klass + '">' + label + '</span>')

    if volunteer.taken:
        return state_tag('taken', ugettext("Užimta"))
    elif volunteer.state:
        state = volunteer.state[0]
        if state.removed:
            return state_tag('removed', ugettext("Pašalinta"))
        elif state.accepted is None:
            return state_tag('invited', ugettext("Pakviesta"))
        elif state.accepted is True:
            return state_tag('accepted', ugettext("Priimta"))
        elif state.accepted is False:
            return state_tag('refused', ugettext("Atsisakė"))
    else:
        return mark_safe(''.join([
            '<a %s>' % ' '.join([
                'href="#"',
                'class="btn btn-default btn-sm"',
                'onclick="savanoriai.toggle_choice(this, \'%s\', %r);"' % (
                    reverse('toggle_choice'),
                    volunteer.pk
                ),
            ]),
            ugettext("Pasirinkti"),
            '</a>'
        ]))
