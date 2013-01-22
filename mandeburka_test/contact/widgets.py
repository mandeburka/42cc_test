from django.forms.widgets import DateInput
from django.utils.safestring import mark_safe


class ContactDateInput(DateInput):
    def render(self, name, value, attrs=None):
        html = super(ContactDateInput, self).render(name, value, attrs)
        return mark_safe(html + '''
<script type="text/javascript">
$(function() {
    $('#%s').datepicker({
      dateFormat: 'yy-mm-dd',
      changeYear: true,
      changeMonth: true
    });
});
</script>
        ''' % attrs['id'])
