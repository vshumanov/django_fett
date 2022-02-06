from django import forms


HEADER = (
    ("name", "name"),
    ("height", "height"),
    ("mass", "mass"),
    ("hair_color", "hair_color"),
    ("skin_color", "skin_color"),
    ("eye_color", "eye_color"),
    ("birth_year", "birth_year"),
    ("gender", "gender"),
    ("homeworld", "homeworld"),
    ("date", "date"),
)


class ValueCountsForm(forms.Form):
    headers_field = forms.MultipleChoiceField(
        choices=HEADER, widget=forms.CheckboxSelectMultiple
    )
