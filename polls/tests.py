from django.test import TestCase, Client


class CreatePoll(TestCase):

    def test_create_simple_poll(self):
        c = Client()
        response = c.post('/polls/poll', {'question_text': 'How are you?'})
        self.assertEqual(response.status_code, 200)
        response = c.post('/polls/poll/', {'question_text': 'And you?'})
        self.assertEqual(response.status_code, 200)

    def test_create_simple_poll_with_wrong_method(self):
        c = Client()
        response = c.get('/polls/poll', {'question_text':
                         'Have you had lunch?'})
        self.assertEqual(response.status_code, 404)

