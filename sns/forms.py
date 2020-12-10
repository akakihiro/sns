from django import forms
from.models import Message,Group,Friend,Good
from django.contrib.auth.models import User

#Messageのフォーム
class MessageForm(forms.ModelForm):
    class Meta:
        model=Message
        fields=['owner','group','content','image']

#Group
class GroupForm(forms.ModelForm):
    class Meta:
        model=Group
        fields=['owner','title']

#Friend
class FriendForm(forms.ModelForm):
    class Meta:
        model=Friend
        fields=['owner','user','group']

#Good
class GoodForm(forms.ModelForm):
    class Meta:
        model=Good
        fields=['owner','message']

#Groupのチェックボックスフォーム
class GroupCheckForm(forms.Form):
    def __init__(self,user,*args,**kwargs):
        super(GroupCheckForm,self).__init__(*args,**kwargs)
        public=User.objects.filter(username='public').first()
        self.fields['groups']=forms.MultipleChoiceField(
            choices=[(item.title,item.title)\
            for item in Group.objects.filter(owner__in=[user,public])],
            widget=forms.CheckboxSelectMultiple(),
        )

#Groupの選択メニューフォーム
class GroupSelectForm(forms.Form):
    def __init__(self,user,*args,**kwargs):
        super(GroupSelectForm,self).__init__(*args,**kwargs)
        self.fields['groups']=forms.ChoiceField(
            choices=[('-','-')]+[(item.title,item.title)\
            for item in Group.objects.filter(owner=user)],
            widget=forms.Select(attrs={'class':'form-control'}),
        )

#Friendのチェックボックスフォーム
class FriendsForm(forms.Form):
    def __init__(self,user,friends=[],vals=[],*args,**kwargs):
        super(FriendsForm,self).__init__(*args,**kwargs)
        self.fields['friends']=forms.MultipleChoiceField(
            choices=[(item.user,item.user) for item in friends],
            widget=forms.CheckboxSelectMultiple(),
            initial=vals
        )

#Group作成フォーム
class CreateGroupForm(forms.Form):
    group_name=forms.CharField(max_length=50,\
    widget=forms.TextInput(attrs={'class':'form-control'}))

#投稿フォーム
class PostForm(forms.Form):
    content=forms.CharField(max_length=500,\
    widget=forms.Textarea(attrs={'class':'form-control','rows':2}))
    image=forms.ImageField(max_length=500,\
    widget=forms.ClearableFileInput(attrs={'multiple':True,\
    'class':'form-control'}),required=False)

    def __init__(self,user,*args,**kwargs):
        super(PostForm,self).__init__(*args,**kwargs)
        public=User.objects.filter(username='public').first()
        self.fields['groups']=forms.ChoiceField(
            choices=[('-','-')]+[(item.title,item.title)\
            for item in Group.objects.\
            filter(owner__in=[user,public])],
            widget=forms.Select(attrs={'class':'form-control'}),
        )

#並べ替えフォーム
class OrderForm(forms.Form):

    order=forms.ChoiceField(
        choices=[('DESC','新しい順'),
                 ('ASC','古い順')],
        widget=forms.Select(attrs={'class':'form-control'}),
    )

#ユーザー登録フォーム
class EntryForm(forms.Form):
    username = forms.CharField(\
    widget=forms.TextInput(attrs={'class':'form-control'}))
    enter_password = forms.CharField(\
    widget=forms.PasswordInput(attrs={'class':'form-control'}))
    retype_password = forms.CharField(\
    widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email=forms.EmailField(\
    widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name=forms.CharField(\
    widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(\
    widget=forms.TextInput(attrs={'class':'form-control'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('このユーザー名は既に使われています。')
        return username

    def clean_enter_password(self):
        password = self.cleaned_data.get('enter_password')
        if len(password) < 5:
            raise forms.ValidationError('パスワードは5文字以上でなくてはなりません。')
        return password

    def clean(self):
        super(EntryForm, self).clean()
        password = self.cleaned_data.get('enter_password')
        retyped = self.cleaned_data.get('retype_password')
        if password and retyped and (password != retyped):
            self.add_error('retype_password', 'パスワードが一致していません。')
    
    def save(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('enter_password')
        email=self.cleaned_data.get('email')
        first_name=self.cleaned_data.get('first_name')
        last_name=self.cleaned_data.get('last_name')
        new_user = User.objects.create_user(username = username)
        new_user.set_password(password)
        new_user.email=email
        new_user.first_name=first_name
        new_user.last_name=last_name
        new_user.is_staff=True
        new_user.save()