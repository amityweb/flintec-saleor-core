from typing import Optional

import graphene
from django.core.exceptions import ValidationError

from ....giftcard.utils import order_has_gift_card_lines
from ....order import FulfillmentStatus, models
from ....order.actions import order_refunded
from ....order.error_codes import OrderErrorCode
<<<<<<< HEAD
from ....payment import PaymentError, TransactionKind, gateway
from ....payment.gateway import request_refund_action
=======
from ....payment import TransactionKind, gateway
from ....payment import models as payment_models
from ....permission.enums import OrderPermissions
from ...app.dataloaders import get_app_promise
from ...core import ResolveInfo
from ...core.doc_category import DOC_CATEGORY_ORDERS
>>>>>>> fa9ea3af1251eaa792bebc0aabcf03f49b31a7e9
from ...core.mutations import BaseMutation
from ...core.scalars import PositiveDecimal
from ...core.types import OrderError
from ...plugins.dataloaders import get_plugin_manager_promise
from ..types import Order
from .utils import clean_payment, try_payment_action


def clean_refund_payment(
    payment: Optional[payment_models.Payment],
) -> payment_models.Payment:
    payment = clean_payment(payment)
    if not payment.can_refund():
        raise ValidationError(
            {
                "payment": ValidationError(
                    "Payment cannot be refunded.",
                    code=OrderErrorCode.CANNOT_REFUND.value,
                )
            }
        )
    return payment


def clean_order_refund(order: models.Order) -> models.Order:
    if order_has_gift_card_lines(order):
        raise ValidationError(
            {
                "id": ValidationError(
                    "Cannot refund order with gift card lines.",
                    code=OrderErrorCode.CANNOT_REFUND.value,
                )
            }
        )
    return order


class OrderRefund(BaseMutation):
    order = graphene.Field(Order, description="A refunded order.")

    class Arguments:
        id = graphene.ID(required=True, description="ID of the order to refund.")
        amount = PositiveDecimal(
            required=True, description="Amount of money to refund."
        )

    class Meta:
        description = "Refund an order."
        doc_category = DOC_CATEGORY_ORDERS
        permissions = (OrderPermissions.MANAGE_ORDERS,)
        error_type_class = OrderError
        error_type_field = "order_errors"

    @classmethod
    def perform_mutation(  # type: ignore[override]
        cls, _root, info: ResolveInfo, /, *, amount, id: str
    ):
        if amount <= 0:
            raise ValidationError(
                {
                    "amount": ValidationError(
                        "Amount should be a positive number.",
                        code=OrderErrorCode.ZERO_QUANTITY.value,
                    )
                }
            )

<<<<<<< HEAD
        order = cls.get_node_or_error(info, data.get("id"), only_type=Order)
        clean_order_refund(order)

        if payment_transactions := list(order.payment_transactions.all()):
            # We use the last transaction as we don't have a possibility to
            # provide way of handling multiple transaction here
            try:
                request_refund_action(
                    payment_transactions[-1],
                    info.context.plugins,
                    refund_value=amount,
                    channel_slug=order.channel.slug,
                    user=info.context.user,
                    app=info.context.app,
                )
            except PaymentError as e:
                raise ValidationError(
                    str(e),
                    code=OrderErrorCode.MISSING_TRANSACTION_ACTION_REQUEST_WEBHOOK,
                )
        else:
            payment = order.get_last_payment()
            clean_payment(payment)
            clean_refund_payment(payment)
            transaction = try_payment_action(
                order,
                info.context.user,
                info.context.app,
=======
        order = cls.get_node_or_error(info, id, only_type=Order)
        cls.check_channel_permissions(info, [order.channel_id])
        order = clean_order_refund(order)
        app = get_app_promise(info.context).get()
        manager = get_plugin_manager_promise(info.context).get()
        payment = order.get_last_payment()
        payment = clean_payment(payment)
        payment = clean_refund_payment(payment)
        transaction = try_payment_action(
            order,
            info.context.user,
            app,
            payment,
            gateway.refund,
            payment,
            manager,
            amount=amount,
            channel_slug=order.channel.slug,
        )
        # Confirm that we changed the status to refund. Some payment can receive
        # asynchronous webhook with update status
        if transaction.kind == TransactionKind.REFUND:
            payment.refresh_from_db()
            order_refunded(
                order,
                info.context.user,
                app,
                amount,
>>>>>>> fa9ea3af1251eaa792bebc0aabcf03f49b31a7e9
                payment,
                manager,
            )
<<<<<<< HEAD
            # Confirm that we changed the status to refund. Some payment can receive
            # asynchronous webhook with update status
            if transaction.kind == TransactionKind.REFUND:
                order_refunded(
                    order,
                    info.context.user,
                    info.context.app,
                    amount,
                    payment,
                    info.context.plugins,
                )
=======
>>>>>>> fa9ea3af1251eaa792bebc0aabcf03f49b31a7e9

        order.fulfillments.create(
            status=FulfillmentStatus.REFUNDED, total_refund_amount=amount
        )
        return OrderRefund(order=order)
