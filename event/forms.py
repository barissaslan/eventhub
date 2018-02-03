from django import forms
from .models import Event
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, MultiField, Div
from ckeditor.widgets import CKEditorWidget


class EventCreateForm(forms.ModelForm):
    start = forms.DateTimeField(widget=forms.TimeInput(format='%Y-%m-%d %H:%M'), label="Starts")
    end = forms.DateTimeField(widget=forms.TimeInput(format='%Y-%m-%d %H:%M'), label="Ends")
    image = forms.FileField(label='Event Image', required=False)
    description = forms.CharField(widget=CKEditorWidget(), label='Event Description', required=False)
    online = forms.BooleanField(label='Online Event')

    def __init__(self, *args, **kwargs):
        super(EventCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Event Details",
                'title',
                'location',
                'online',
                Div(
                    Div('start', css_class='col-md-6', ),
                    Div('end', css_class='col-md-6', ),
                    css_class='row',

                ),
                'image',
                'description',
                'organizer_name',
            ),
            Fieldset(
                "Create Tickets",
                'capacity',
            ),
            Fieldset(
                "Additional Settings",
                'event_type',
                'event_topic',
            ),
            # ButtonHolder(
            #     Submit('submit', 'Submit', css_class='btn btn-primary')
            # )
        )

    class Meta:

        model = Event
        fields = [
            'title',
            'location',
            'online',
            'start',
            'end',
            'image',
            'organizer_name',
            'description',
            'event_type',
            'event_topic',
            'capacity',
        ]


class EventRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(EventRegisterForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                "Attendee Information",
                'first_name',
                'last_name',
            ),
            Fieldset(
                "Permission",
                'email',
            ),
            # ButtonHolder(
            #     Submit('submit', 'Submit', css_class='btn btn-primary')
            # )
        )


