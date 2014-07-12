from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from polls.models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        pass


class LastQuestionView(generic.ListView):
    template_name = 'polls/question_list.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))


def index(request):
    return render(request, 'polls/index.html')


def create_poll(request):
    if not request.POST:
        raise Http404
    else:
        if request.POST['question_text']:
            q = Question(question_text=request.POST['question_text'],
                         pub_date=timezone.now())
            q.save()
            return HttpResponseRedirect(reverse('polls:create_choices',
                                                args=(q.id,)))
        else:
           return render(request, 'polls/index.html', {
                'error_message': 'The question cannot be empty.',
                })

def create_choices(request, question_id):
    if not request.POST:
        q = get_object_or_404(Question, pk=question_id)
        return render(request, 'polls/create_question.html',
                      {'question': q})
    else:
        q = get_object_or_404(Question, pk=question_id)
        if request.POST['answer_text_1'] and request.POST['answer_text_2']:
            q.choice_set.create(choice_text=request.POST['answer_text_1'],
                                votes=0)
            q.choice_set.create(choice_text=request.POST['answer_text_2'],
                                votes=0)
            return HttpResponseRedirect(reverse('polls:last_question_view',))

        else:
            return render(request, 'polls/create_question.html',
                          {'question': q,
                           'error_message': 'At least two possible answers '
                                            'are needed'})
