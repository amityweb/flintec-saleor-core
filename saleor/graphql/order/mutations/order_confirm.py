from typing import cast

import graphene
from django.core.exceptions import ValidationError
from django.db import transaction

from ....account.models import User
from ....core.tracing import traced_atomic_transaction
from ....order import OrderStatus, models
from ....order.actions import order_charged, order_confirmed
from ....order.error_codes import OrderErrorCode
from ....order.fetch import fetch_order_info
<<<<<<< HEAD
from ....payment import PaymentError, gateway
from ....payment.gateway import request_charge_action
=======
from ....order.utils import update_order_display_gross_prices
from ....payment import gateway
from ....permission.enums import OrderPermissions
from ...app.dataloaders import get_app_promise
from ...core import ResolveInfo
>>>>>>> fa9ea3af1251eaa792bebc0aabcf03f49b31a7e9
from ...core.mutations import ModelMutation
from ...core.types import OrderError
from ...plugins.dataloaders import get_plugin_manager_promise
from ...site.dataloaders import get_site_promise
from ..types import Order


class OrderConfirm(ModelMutation):
    order = graphene.Field(Order, description="Order which has been confirmed.")

    class Arguments:
        id = graphene.ID(description="ID of an order to confirm.", required=True)

    class Meta:
        description = "Confirms an unconfirmed order by changing status to unfulfilled."
        model = models.Order
        object_type = Order
        permissions = (OrderPermissions.MANAGE_ORDERS,)
        error_type_class = OrderError
        error_type_field = "order_errors"

    @classmethod
    def get_instance(cls, info: ResolveInfo, **data):
        instance = super().get_instance(info, **data)
        if not instance.is_unconfirmed():
            raise ValidationError(
                {
                    "id": ValidationError(
                        "Provided order id belongs to an order with status "
                        "different than unconfirmed.",
                        code=OrderErrorCode.INVALID.value,
                    )
                }
            )
        if not instance.lines.exists():
            raise ValidationError(
                {
                    "id": ValidationError(
                        "Provided order id belongs to an order without products.",
                        code=OrderErrorCode.INVALID.value,
                    )
                }
            )
        return instance

    @classmethod
    def perform_mutation(cls, root, info: ResolveInfo, /, **data):
        user = info.context.user
        user = cast(User, user)
        order = cls.get_instance(info, **data)
        cls.check_channel_permissions(info, [order.channel_id])
        order.status = OrderStatus.UNFULFILLED
        update_order_display_gross_prices(order)
        order.save(update_fields=["status", "updated_at", "display_gross_prices"])
        order_info = fetch_order_info(order)
        payment = order_info.payment
<<<<<<< HEAD
        manager = info.context.plugins
        if payment_transactions := list(order.payment_transactions.all()):
            try:
                # We use the last transaction as we don't have a possibility to
                # provide way of handling multiple transaction here
                payment_transaction = payment_transactions[-1]
                request_charge_action(
                    transaction=payment_transaction,
                    manager=info.context.plugins,
                    charge_value=payment_transaction.authorized_value,
                    channel_slug=order.channel.slug,
                    user=info.context.user,
                    app=info.context.app,
=======
        manager = get_plugin_manager_promise(info.context).get()
        app = get_app_promise(info.context).get()
        with traced_atomic_transaction():
            if payment and payment.is_authorized and payment.can_capture():
                authorized_payment = payment
                gateway.capture(payment, manager, channel_slug=order.channel.slug)
                site = get_site_promise(info.context).get()
                transaction.on_commit(
                    lambda: order_charged(
                        order_info,
                        info.context.user,
                        app,
                        authorized_payment.total,
                        authorized_payment,
                        manager,
                        site.settings,
                    )
>>>>>>> fa9ea3af1251eaa792bebc0aabcf03f49b31a7e9
                )
            transaction.on_commit(
<<<<<<< HEAD
                lambda: order_captured(
                    order_info,
                    info.context.user,
                    info.context.app,
                    payment.total,
                    payment,
=======
                lambda: order_confirmed(
                    order,
                    user,
                    app,
>>>>>>> fa9ea3af1251eaa792bebc0aabcf03f49b31a7e9
                    manager,
                    send_confirmation_email=True,
                )
            )
<<<<<<< HEAD
        transaction.on_commit(
            lambda: order_confirmed(
                order,
                info.context.user,
                info.context.app,
                manager,
                send_confirmation_email=True,
            )
        )
=======
>>>>>>> fa9ea3af1251eaa792bebc0aabcf03f49b31a7e9
        return OrderConfirm(order=order)
