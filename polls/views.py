from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse

from .models import Question

# Create your views here.
def index(request) -> HttpResponse:
    latest_questions = Question.objects.order_by("-publication_date")[:5]
    context = { "latest_questions": latest_questions }
    return render(request, "polls/index.html", context)

def detail(request, question_id) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    q = Question.objects.get(pk=1)
    return render(request, "polls/detail.html", { "question": question })

def results(request, question_id) -> HttpResponse:
    return HttpResponse(f"You are looking at the results of {question_id}")

def vote(request, question_id) -> HttpResponse:
    return HttpResponse(f"You are voting on question {question_id}")
