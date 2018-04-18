from django import forms


class CategoryForm(forms.Form):
    category_name = forms.CharField(label='',
                                    max_length=30,
                                    widget=forms.TextInput(attrs={'placeholder': 'Catgory Name'}))

    category_descr = forms.CharField(label='',
                                     required=False,
                                     max_length=100,
                                     widget=forms.TextInput(attrs={'placeholder': 'Category Description'}))


class ProductForm(forms.Form):
    product_name = forms.CharField(label='',
                                   required=True,
                                   max_length=30,
                                   widget=forms.TextInput(attrs={'placeholder': 'Product Name'}))

    product_specs = forms.CharField(label='',
                                    required=True,
                                    max_length=30,
                                    widget=forms.TextInput(attrs={'placeholder': 'Product Specs'}))

    product_price = forms.DecimalField(label='',
                                       required=True,
                                       max_digits=20, decimal_places=3,
                                       min_value=0.0,
                                       widget=forms.NumberInput(attrs={'placeholder': 'Product Price'}))

    number_in_stock = forms.IntegerField(label='',
                                         required=True,
                                         min_value=0,
                                         widget=forms.NumberInput(attrs={'placeholder': 'Number in Stock'}))


SEARCH_TYPE = (
    ('C', 'Category'),
    ('P', 'Product'),
    ('S', 'Store'),
)


class SearchForm(forms.Form):
    search_item = forms.CharField(label='',
                                  required=True,
                                  max_length=20,
                                  widget=forms.TextInput(attrs={'placeholder': 'Search Item'}))

    search_filter = forms.MultipleChoiceField(label='',
                                              required=True,
                                              choices=SEARCH_TYPE,
                                              widget=forms.CheckboxSelectMultiple)
