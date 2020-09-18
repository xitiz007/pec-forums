from .models import Question, Answer
from django.forms import ModelForm, Textarea

class CreateQuestion(ModelForm):
    class Meta:
        model = Question
        fields = ['question_title', 'faculty']
        labels = {
            'question_title' : 'Question',
            'faculty' : 'Post in'
        }

    def __init__(self, *args, **kwargs):
        super(CreateQuestion, self).__init__(*args, **kwargs)
        self.fields['question_title'].widget.attrs['cols'] = 3
        self.fields['question_title'].widget.attrs['rows'] = 3
        self.fields['question_title'].widget.attrs['placeholder'] = 'write down your question here......'

class CreateAnswer(ModelForm):
    class Meta:
        model = Answer
        fields = ['answer']
        labels = {
            'answer' : ''
        }
        
    def __init__(self, *args, **kwargs):
        super(CreateAnswer, self).__init__(*args, **kwargs)
        self.fields['answer'].widget.attrs['cols'] = 2
        self.fields['answer'].widget.attrs['rows'] = 2
        self.fields['answer'].widget.attrs['placeholder'] = 'write down your answer here...'
