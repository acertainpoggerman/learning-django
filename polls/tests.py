from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

import datetime

from .models import Question

# TODO: Make sure all tests successfully complete

# Shortcut to create questions
def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question(question_text=question_text, publication_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exists, should display appropriate message
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available")
        self.assertQuerySetEqual(response.context["latest_questions"], [])

    def test_past_question(self):
        """
        Questions with a publication date are displayed
        on the page
        """
        question = create_question("This is a question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_questions"],
            [question]
        )

    def test_future_question(self):
        """
        Questions having publication_date in the future
        aren't displayed on the index page
        """
        create_question("This is a question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls available")
        self.assertQuerySetEqual(response.context["latest_questions"], [])

    def test_future_question_and_past_question(self):
        """
        When both past and future questions are displayed, only past
        questions are displayed
        """
        question = create_question("This is the past question", days=-30)
        create_question("This is the future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_questions"],
            [question]
        )

    def test_two_past_questions(self):
        """
        The index page displays both past questions
        """
        question1 = create_question("This is the 1st question", days=-20)
        question2 = create_question("This is the 2nd question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_questions"],
            [question1, question2]
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question("This is a future question", days=30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question("This is a past question", days=-30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response.content, past_question.question_text)


# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose publication_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(publication_date=time)
        self.assertIs(future_question.was_published_recently(), False)


    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose publication_date is older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(publication_date=time)
        self.assertIs(old_question.was_published_recently(), False)


    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose publication_date is within the last day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(publication_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
