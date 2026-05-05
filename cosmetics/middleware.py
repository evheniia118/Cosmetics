from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import UserSession

class SessionTrackingMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated:

            if not request.session.get('login_time'):
                request.session['login_time'] = timezone.now().timestamp()

                session = UserSession.objects.create(
                    user=request.user,
                    login_time=timezone.now()
                )
                request.session['session_id'] = session.id

            raw_login_time = request.session.get('login_time')

            try:
                login_time = float(raw_login_time)
            except:
                request.session['login_time'] = timezone.now().timestamp()
                login_time = float(request.session['login_time'])

            duration = int(timezone.now().timestamp() - login_time)
            request.session['session_duration'] = duration
