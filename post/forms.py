from django import forms
from post.models import Post

class FazerPostForm(forms.Form):
    texto = forms.CharField(required=True)

    def is_valid(self):
        valid = True
        if not super(FazerPostForm, self).is_valid():
            self.adiciona_erro('Teste')
            valid = False
        
        return valid