from django import forms
from tasks.models import Event,Category

class StyledFormMixin:
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()  
    """Mixing to apply style to form field"""
    default_classes="border-2 mt-6 rounded-lg shadow-sm w-1/2 p-3 border-gray-300 "
    "focus:outline-none focus:border-rose-300 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter{field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class':"border-2 rounded-lg shadow-sm  p-3 border-gray-300 "
                    "focus:outline-none focus:border-rose-300 focus:ring-rose-500",
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class':"space-y-2",
                })
            else:
                field.widget.attrs.update({
                    'class':self.default_classes,
                })

class EventForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model=Event
        fields=[
            'name','description',
            'date','time',
            'location',
            'asset'
            ]
        widgets={
                'date':forms.DateInput(attrs={'type':'date'}),
                'time': forms.TimeInput(attrs={'type': 'time'}),
                'description': forms.Textarea(attrs={'rows': 3}),
            }
    
class CategoryForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model=Category
        fields=['name','description']   
      


        