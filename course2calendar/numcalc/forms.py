from django import forms


class HTMLFileForm(forms.Form):
    """用于上传课程表HTML文件的表单"""
    file = forms.FileField(
        label="选择HTML文件",
        help_text="上传课程表HTML文件，系统会生成日历文件",
        widget=forms.FileInput(attrs={'accept': '.html'})
    ) 