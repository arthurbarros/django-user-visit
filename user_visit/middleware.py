import logging
import typing
import uuid
import django.db
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpRequest, HttpResponse
from django.utils import timezone

from user_visit.models import UserVisit

from .settings import RECORDING_BYPASS, RECORDING_DISABLED

logger = logging.getLogger(__name__)


def save_user_visit(user_visit: UserVisit) -> None:
    """Save the user visit and handle db.IntegrityError."""
    try:
        user_visit.save()
    except django.db.IntegrityError:
        logger.warning("Error saving user visit (hash='%s')", user_visit.hash)


class UserVisitMiddleware:
    """Middleware to record user visits."""

    def __init__(self, get_response: typing.Callable) -> None:
        if RECORDING_DISABLED:
            raise MiddlewareNotUsed("UserVisit recording has been disabled")
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> typing.Optional[HttpResponse]:
        user_cookie_id = request.COOKIES.get('user_cookie_id', str(uuid.uuid4())) 

        if request.user.is_anonymous:
            return self.get_response(request)

        if RECORDING_BYPASS(request):
            return self.get_response(request)

        uv = UserVisit.objects.build(request, timezone.now(), user_cookie_id)
        if not UserVisit.objects.filter(hash=uv.hash).exists():
            save_user_visit(uv)
        response = self.get_response(request)
        response.set_cookie('user_cookie_id', uv.user_cookie_id)
        return response