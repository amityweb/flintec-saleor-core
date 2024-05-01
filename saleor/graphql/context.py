from typing import Optional, cast

from django.contrib.auth import authenticate
<<<<<<< HEAD
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AnonymousUser
from django.db.models import Exists, OuterRef
=======
from django.http import HttpRequest
from django.utils import timezone
>>>>>>> fa9ea3af1251eaa792bebc0aabcf03f49b31a7e9
from django.utils.functional import SimpleLazyObject

from ..account.models import User
from ..app.models import App, AppToken
from ..core.auth import get_token_from_request
from ..core.jwt import jwt_decode_with_exception_handler
from .api import API_PATH
<<<<<<< HEAD
=======
from .app.dataloaders import get_app_promise
from .core import SaleorContext
>>>>>>> fa9ea3af1251eaa792bebc0aabcf03f49b31a7e9


def get_context_value(request: HttpRequest) -> SaleorContext:
    request = cast(SaleorContext, request)
    if not hasattr(request, "dataloaders"):
        request.dataloaders = {}
    request.allow_replica = getattr(request, "allow_replica", True)
    request.request_time = getattr(request, "request_time", timezone.now())
    set_app_on_context(request)
    set_auth_on_context(request)
    set_decoded_auth_token(request)
    return request


class RequestWithUser(HttpRequest):
    _cached_user: Optional[User]
    app: Optional[App]
<<<<<<< HEAD
    user: Union[UserType, SimpleLazyObject]


def get_app(raw_auth_token) -> Optional[App]:
    tokens = AppToken.objects.filter(token_last_4=raw_auth_token[-4:]).values_list(
        "id", "auth_token"
    )
    token_ids = [
        id for id, auth_token in tokens if check_password(raw_auth_token, auth_token)
    ]
    return App.objects.filter(
        Exists(tokens.filter(id__in=token_ids, app_id=OuterRef("pk"))), is_active=True
    ).first()


def set_decoded_auth_token(request):
    token = get_token_from_request(request)
    decoded_auth_token = jwt_decode_with_exception_handler(token)
    request.decoded_auth_token = decoded_auth_token
=======


def set_decoded_auth_token(request: SaleorContext):
    auth_token = get_token_from_request(request)
    if auth_token:
        request.decoded_auth_token = jwt_decode_with_exception_handler(auth_token)
    else:
        request.decoded_auth_token = None
>>>>>>> fa9ea3af1251eaa792bebc0aabcf03f49b31a7e9


def set_app_on_context(request: SaleorContext):
    if request.path == API_PATH and not hasattr(request, "app"):
<<<<<<< HEAD
        request.app = None
        auth_token = get_token_from_request(request)
        if auth_token and len(auth_token) == 30:
            request.app = SimpleLazyObject(lambda: get_app(auth_token))
=======
        request.app = get_app_promise(request).get()
>>>>>>> fa9ea3af1251eaa792bebc0aabcf03f49b31a7e9


def get_user(request: SaleorContext) -> Optional[User]:
    if not hasattr(request, "_cached_user"):
        request._cached_user = cast(Optional[User], authenticate(request=request))
    return request._cached_user


def set_auth_on_context(request: SaleorContext):
    if hasattr(request, "app") and request.app:
        request.user = SimpleLazyObject(lambda: None)  # type: ignore
        return request

    def user():
        return get_user(request) or None

    request.user = SimpleLazyObject(user)  # type: ignore
