from django import forms
from .models import Project, Review


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "featured_image",
            "description",
            "demo_link",
            "source_link",
        ]
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        # self.fields["title"].widget.attrs.update({"class": "input input--text"})
        # self.fields["description"].widget.attrs.update({"class": "input input--text"})
        # self.fields["title"].widget.attrs.update({"class": "input input--text"})
        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "input input--text"})


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["value", "body"]

        labels = {"value": "Place your vote", "body": "Add a comment with your vote"}

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        # self.fields["title"].widget.attrs.update({"class": "input input--text"})
        # self.fields["description"].widget.attrs.update({"class": "input input--text"})
        # self.fields["title"].widget.attrs.update({"class": "input input--text"})
        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "input input--text"})
