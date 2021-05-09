from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

#using passresttoken to generate our token
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return(
        six.text_type(user.pk) + six.text_type(timestamp) +
        six.text_type(user.userprofile.email_confirmed)
        )

#call funtion to activate token
account_activation_token = AccountActivationTokenGenerator()
