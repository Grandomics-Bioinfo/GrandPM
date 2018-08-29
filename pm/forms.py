#from django.forms import ModelForm, Textarea
from django import forms

from django.utils.translation import ugettext_lazy as _

class ProjectForm(forms.ModelForm):
    Analysis_Typeaa = (
        ('met', _('甲基化aaa')),
        ('sv', _('结构变异')),
        ('str', _('串联重复')),
        ('tumor', _('肿瘤')),
        ('haplotype', _('单体型'))
    )

    analysis_type = forms.MultipleChoiceField( 
                                           choices=Analysis_Typeaa, 
                                           widget=forms.CheckboxSelectMultiple())

