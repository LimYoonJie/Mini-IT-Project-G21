from django import forms

from .categories import CATEGORY_GROUPS
from .models import Product


class ProductAdminForm(forms.ModelForm):
    category = forms.ChoiceField(choices=[])

    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(group, [(category, category) for category in categories]) for group, categories in CATEGORY_GROUPS.items()]
        current_category = self.instance.category
        known_categories = {
            category for categories in CATEGORY_GROUPS.values() for category in categories
        }
        if self.instance.pk and current_category and current_category not in known_categories:
            choices.insert(0, ("Existing category", [(current_category, current_category)]))
        self.fields["category"].choices = [("", "Select a category"), *choices]