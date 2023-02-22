from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def get_choice_from_request(choice, question):
        return question.choice_set.get(pk=choice)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice = get_choice_from_request(request.POST['choice'], question)
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice",
        })
    choice.votes += 1
    choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
