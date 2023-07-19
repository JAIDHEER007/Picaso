from django import forms

class promtForm(forms.Form):
    prompt = forms.CharField(label="", widget=forms.Textarea(attrs={"rows":5, "cols":50}))