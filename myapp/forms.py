from django import forms
from django.forms import PasswordInput

from myapp.models import Order, Review, Student


class SearchForm(forms.Form):
    LENGTH_CHOICES = [
        (8, '8 Weeks'),
        (10, '10 Weeks'),
        (12, '12 Weeks'),
        (14, '14 Weeks'),
    ]
    name = forms.CharField(max_length=100, required=False, label="Student Name:")
    length = forms.TypedChoiceField(widget=forms.RadioSelect,choices=LENGTH_CHOICES,label="Preferred course duration:", coerce=int,required=False)
    max_price = forms.IntegerField(min_value=0,label="Maximum Price")

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['courses', 'Student', 'order_status']
        widgets = {'courses': forms.CheckboxSelectMultiple(),
                   'order_type': forms.RadioSelect}
        labels = {'student': u'Student Name' }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'course', 'rating', 'comments']
        widgets = {'course':forms.RadioSelect}
        labels = {'reviewer': u'Please enter a valid email',
                  'rating':u'Rating: An integer between 1 (worst) and 5 (best)'}
    def __init__(self,*args,**kwargs):
        super(ReviewForm, self).__init__(*args,**kwargs)
        self.fields['course'].empty_label=None

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields=['username', 'password','first_name','last_name', 'address', 'interested_in']
        widgets = {'interested_in': forms.CheckboxSelectMultiple(),'password':forms.PasswordInput()}
        labels={
            'username':u'Username:',
            'passowrd':u'Passowrd:',
            'first_name':u'First Name:',
            'last_name': u'Last Name:',
            'address' : u'City:',
            'interested_in': u'Courses you are interested in:'
        }
        
    def __init__(self,*args,**kwargs):
        super(RegisterForm, self).__init__(*args,**kwargs)
        self.fields['interested_in'].empty_label=None
