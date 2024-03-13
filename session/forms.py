from django import forms

class QuestionForm(forms.Form):
    question_1 = forms.CharField(required=False)
    question_2 = forms.CharField(required=False)
    question_3 = forms.CharField(required=False)
    question_4 = forms.CharField(required=False)

class RespiratoryGraphForm(forms.Form):
    csv_input = forms.CharField()
    time_input = forms.CharField()
    
class SustainedAttentionForm(forms.Form):
    csv_input = forms.CharField()
    rate_input = forms.JSONField(required=False)
    time_input = forms.CharField()
    
class GuidedMeditationForm(forms.Form):
    lecture_input = forms.CharField(required=False)