from datetime import timedelta
from django.utils import timezone

from locarise_drf_oauth2_support.users.models import User

try:
    import factory

    class UserF(factory.DjangoModelFactory):
        first_name = factory.Sequence(lambda n: "first_name%s" % n)
        last_name = factory.Sequence(lambda n: "last_name%s" % n)
        email = factory.Sequence(lambda n: "email%s@example.com" % n)
        is_staff = False
        is_active = True
        is_superuser = False
        last_login = timezone.now() - timedelta(days=2)
        password = factory.PostGenerationMethodCall('set_password', 'pass')

        class Meta:
            model = User

except ImportError:  # pragma: no cover
    pass
