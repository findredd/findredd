from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email

        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, instance, timestamp):
        return (text_type(instance.is_active) + text_type(instance.pk) + text_type(timestamp))
