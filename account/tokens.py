from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class PasswordTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return ''.join(
            map(six.text_type, [user.pk, timestamp, user.is_active])
        )


password_token = PasswordTokenGenerator()
