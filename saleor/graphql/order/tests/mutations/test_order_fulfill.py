from unittest.mock import ANY, patch

import graphene
import pytest

from .....core.exceptions import InsufficientStock, InsufficientStockData
from .....giftcard import GiftCardEvents
from .....giftcard.models import GiftCard, GiftCardEvent
from .....order import FulfillmentStatus, OrderStatus
from .....order.error_codes import OrderErrorCode
from .....order.models import Fulfillment, FulfillmentLine
from .....product.models import ProductVariant
from .....tests.utils import flush_post_commit_hooks
from .....warehouse.models import Allocation, Stock
from .....webhook.event_types import WebhookEventAsyncType
from ....tests.utils import assert_no_permission, get_graphql_content

ORDER_FULFILL_MUTATION = """
    mutation fulfillOrder(
        $order: ID, $input: OrderFulfillInput!
    ) {
        orderFulfill(
            order: $order,
            input: $input
        ) {
            fulfillments {
                id
            }
            errors {
                field
                code
                message
                warehouse
                orderLines
            }
        }
    }
"""


@patch("saleor.plugins.manager.PluginsManager.product_variant_out_of_stock")
def test_order_fulfill_with_out_of_stock_webhook(
    product_variant_out_of_stock_webhooks,
    staff_api_client,
    order_with_lines,
    permission_group_manage_orders,
    warehouse,
):
    order = order_with_lines

    query = ORDER_FULFILL_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order_id = graphene.Node.to_global_id("Order", order.id)
    _, order_line2 = order.lines.all()
    order_line2_id = graphene.Node.to_global_id("OrderLine", order_line2.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    variables = {
        "order": order_id,
        "input": {
            "notifyCustomer": True,
            "lines": [
                {
                    "orderLineId": order_line2_id,
                    "stocks": [{"quantity": 2, "warehouse": warehouse_id}],
                },
            ],
        },
    }
    staff_api_client.post_graphql(query, variables)

    stock = order_line2.variant.stocks.filter(warehouse=warehouse).first()
    product_variant_out_of_stock_webhooks.assert_called_once_with(stock)


@pytest.mark.parametrize("fulfillment_auto_approve", [True, False])
@patch("saleor.plugins.manager.PluginsManager.tracking_number_updated")
@patch("saleor.graphql.order.mutations.order_fulfill.create_fulfillments")
def test_order_fulfill(
    mock_create_fulfillments,
    mocked_fulfillment_tracking_number_updated_event,
    fulfillment_auto_approve,
    staff_api_client,
    staff_user,
    order_with_lines,
    permission_group_manage_orders,
    warehouse,
    site_settings,
):
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    site_settings.fulfillment_auto_approve = fulfillment_auto_approve
    site_settings.save(update_fields=["fulfillment_auto_approve"])
    order = order_with_lines
    query = ORDER_FULFILL_MUTATION
    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line, order_line2 = order.lines.all()
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    order_line2_id = graphene.Node.to_global_id("OrderLine", order_line2.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    variables = {
        "order": order_id,
        "input": {
            "notifyCustomer": True,
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 3, "warehouse": warehouse_id}],
                },
                {
                    "orderLineId": order_line2_id,
                    "stocks": [{"quantity": 2, "warehouse": warehouse_id}],
                },
            ],
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert not data["errors"]

    fulfillment_lines_for_warehouses = {
        warehouse.pk: [
            {"order_line": order_line, "quantity": 3},
            {"order_line": order_line2, "quantity": 2},
        ]
    }
    mock_create_fulfillments.assert_called_once_with(
        staff_user,
        None,
        order,
        fulfillment_lines_for_warehouses,
        ANY,
        site_settings,
        True,
        allow_stock_to_be_exceeded=False,
        approved=fulfillment_auto_approve,
        tracking_number="",
    )
    mocked_fulfillment_tracking_number_updated_event.assert_not_called()


def test_order_fulfill_no_channel_access(
    staff_api_client,
    order_with_lines,
    permission_group_all_perms_channel_USD_only,
    warehouse,
    site_settings,
    channel_PLN,
):
    # given
    permission_group_all_perms_channel_USD_only.user_set.add(staff_api_client.user)
    order = order_with_lines
    query = ORDER_FULFILL_MUTATION

    order.channel = channel_PLN
    order.save(update_fields=["channel"])

    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line, order_line2 = order.lines.all()
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    order_line2_id = graphene.Node.to_global_id("OrderLine", order_line2.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    variables = {
        "order": order_id,
        "input": {
            "notifyCustomer": True,
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 3, "warehouse": warehouse_id}],
                },
                {
                    "orderLineId": order_line2_id,
                    "stocks": [{"quantity": 2, "warehouse": warehouse_id}],
                },
            ],
        },
    }

    # when
    response = staff_api_client.post_graphql(query, variables)

    # then
    assert_no_permission(response)


@pytest.mark.parametrize("fulfillment_auto_approve", [True, False])
@patch("saleor.graphql.order.mutations.order_fulfill.create_fulfillments")
def test_order_fulfill_with_tracking_number(
    mock_create_fulfillments,
    fulfillment_auto_approve,
    staff_api_client,
    staff_user,
    order_with_lines,
    permission_group_manage_orders,
    warehouse,
    site_settings,
):
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    site_settings.fulfillment_auto_approve = fulfillment_auto_approve
    site_settings.save(update_fields=["fulfillment_auto_approve"])
    order = order_with_lines
    query = ORDER_FULFILL_MUTATION
    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line, order_line2 = order.lines.all()
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    order_line2_id = graphene.Node.to_global_id("OrderLine", order_line2.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    variables = {
        "order": order_id,
        "input": {
            "notifyCustomer": True,
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 3, "warehouse": warehouse_id}],
                },
                {
                    "orderLineId": order_line2_id,
                    "stocks": [{"quantity": 2, "warehouse": warehouse_id}],
                },
            ],
            "trackingNumber": "test_tracking_number",
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert not data["errors"]

    fulfillment_lines_for_warehouses = {
        warehouse.pk: [
            {"order_line": order_line, "quantity": 3},
            {"order_line": order_line2, "quantity": 2},
        ]
    }
    mock_create_fulfillments.assert_called_once_with(
        staff_user,
        None,
        order,
        fulfillment_lines_for_warehouses,
        ANY,
        site_settings,
        True,
        allow_stock_to_be_exceeded=False,
        approved=fulfillment_auto_approve,
        tracking_number="test_tracking_number",
    )


def test_order_fulfill_with_stock_exceeded_with_flag_disabled(
    staff_api_client,
    staff_user,
    order_with_lines,
    permission_group_manage_orders,
    warehouse,
):
    order = order_with_lines
    query = ORDER_FULFILL_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line, order_line2 = order.lines.all()
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    order_line2_id = graphene.Node.to_global_id("OrderLine", order_line2.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)

    # set stocks to out of quantity and assert
    Stock.objects.filter(warehouse=warehouse).update(quantity=0)

    # make first stock quantity < 0
    stock = Stock.objects.filter(warehouse=warehouse).first()
    stock.quantity = -99
    stock.save()

    for stock in Stock.objects.filter(warehouse=warehouse):
        assert stock.quantity <= 0

    variables = {
        "order": order_id,
        "input": {
            "notifyCustomer": False,
            "allowStockToBeExceeded": False,
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 3, "warehouse": warehouse_id}],
                },
                {
                    "orderLineId": order_line2_id,
                    "stocks": [{"quantity": 2, "warehouse": warehouse_id}],
                },
            ],
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert data["errors"]

    errors = data["errors"]
    assert errors[0]["code"] == "INSUFFICIENT_STOCK"
    assert errors[0]["message"] == "Insufficient product stock."
    assert errors[1]["orderLines"] == [order_line2_id]

    assert errors[1]["code"] == "INSUFFICIENT_STOCK"
    assert errors[1]["message"] == "Insufficient product stock."
    assert errors[1]["orderLines"] == [order_line2_id]


def test_order_fulfill_with_stock_exceeded_with_flag_enabled(
    staff_api_client,
    staff_user,
    order_with_lines,
    permission_group_manage_orders,
    warehouse,
):
    order = order_with_lines
    query = ORDER_FULFILL_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line, order_line2 = order.lines.all()
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    order_line2_id = graphene.Node.to_global_id("OrderLine", order_line2.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)

    # set stocks to out of quantity and assert
    Stock.objects.filter(warehouse=warehouse).update(quantity=0)
    for stock in Stock.objects.filter(warehouse=warehouse):
        assert stock.quantity == 0

    variables = {
        "order": order_id,
        "input": {
            "notifyCustomer": False,
            "allowStockToBeExceeded": True,
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 3, "warehouse": warehouse_id}],
                },
                {
                    "orderLineId": order_line2_id,
                    "stocks": [{"quantity": 2, "warehouse": warehouse_id}],
                },
            ],
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert not data["errors"]

    order.refresh_from_db()

    assert order.status == OrderStatus.FULFILLED

    order_lines = order.lines.all()
    assert order_lines[0].quantity_fulfilled == 3
    assert order_lines[0].quantity_unfulfilled == 0

    assert order_lines[1].quantity_fulfilled == 2
    assert order_lines[1].quantity_unfulfilled == 0

    # check if stocks quantity are < 0 after fulfillments
    for stock in Stock.objects.filter(warehouse=warehouse):
        assert stock.quantity < 0


def test_order_fulfill_with_allow_stock_to_be_exceeded_flag_enabled_and_deleted_stocks(
    staff_api_client, staff_user, permission_group_manage_orders, order_fulfill_data
):
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order = order_fulfill_data.order

    Stock.objects.filter(warehouse=order_fulfill_data.warehouse).delete()

    response = staff_api_client.post_graphql(
        ORDER_FULFILL_MUTATION,
        order_fulfill_data.variables,
    )
    get_graphql_content(response)
    order.refresh_from_db()

    assert order.status == OrderStatus.FULFILLED
    order_lines = order.lines.all()
    assert order_lines[0].quantity_fulfilled == 3
    assert order_lines[0].quantity_unfulfilled == 0

    assert order_lines[1].quantity_fulfilled == 2
    assert order_lines[1].quantity_unfulfilled == 0


def test_order_fulfill_with_allow_stock_to_be_exceeded_flag_disabled_deleted_stocks(
    staff_api_client, staff_user, permission_group_manage_orders, order_fulfill_data
):
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order = order_fulfill_data.order
    order_fulfill_data.variables["input"]["allowStockToBeExceeded"] = False

    Stock.objects.filter(warehouse=order_fulfill_data.warehouse).delete()

    response = staff_api_client.post_graphql(
        ORDER_FULFILL_MUTATION,
        order_fulfill_data.variables,
    )
    get_graphql_content(response)
    order.refresh_from_db()

    assert not order.status == OrderStatus.FULFILLED

    order_lines = order.lines.all()
    assert order_lines[0].quantity_fulfilled == 0
    assert order_lines[0].quantity_unfulfilled == 3

    assert order_lines[1].quantity_fulfilled == 0
    assert order_lines[1].quantity_unfulfilled == 2


def test_order_fulfill_with_allow_stock_to_be_exceeded_flag_enabled_and_deleted_variant(
    staff_api_client, staff_user, permission_group_manage_orders, order_fulfill_data
):
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order = order_fulfill_data.order

    order.lines.first().variant.delete()

    response = staff_api_client.post_graphql(
        ORDER_FULFILL_MUTATION,
        order_fulfill_data.variables,
    )
    get_graphql_content(response)
    order.refresh_from_db()

    assert order.status == OrderStatus.FULFILLED
    order_lines = order.lines.all()
    assert order_lines[0].quantity_fulfilled == 3
    assert order_lines[0].quantity_unfulfilled == 0

    assert order_lines[1].quantity_fulfilled == 2
    assert order_lines[1].quantity_unfulfilled == 0


def test_order_fulfill_with_allow_stock_to_be_exceeded_flag_disabled_deleted_variant(
    staff_api_client, staff_user, permission_group_manage_orders, order_fulfill_data
):
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order = order_fulfill_data.order
    order_fulfill_data.variables["input"]["allowStockToBeExceeded"] = False

    order.lines.first().variant.delete()

    response = staff_api_client.post_graphql(
        ORDER_FULFILL_MUTATION,
        order_fulfill_data.variables,
    )
    get_graphql_content(response)
    order.refresh_from_db()

    assert not order.status == OrderStatus.FULFILLED

    order_lines = order.lines.all()
    assert order_lines[0].quantity_fulfilled == 0
    assert order_lines[0].quantity_unfulfilled == 3

    assert order_lines[1].quantity_fulfilled == 0
    assert order_lines[1].quantity_unfulfilled == 2


@patch("saleor.graphql.order.mutations.order_fulfill.create_fulfillments")
def test_order_fulfill_above_available_quantity(
    mock_create_fulfillments,
    staff_api_client,
    staff_user,
    order_with_lines,
    permission_group_manage_orders,
    warehouse,
):
    order = order_with_lines
    query = ORDER_FULFILL_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line, order_line2 = order.lines.all()
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    order_line2_id = graphene.Node.to_global_id("OrderLine", order_line2.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    fulfillment = Fulfillment.objects.create(
        order=order, status=FulfillmentStatus.WAITING_FOR_APPROVAL
    )
    FulfillmentLine.objects.create(
        order_line=order_line,
        quantity=1,
        stock=warehouse.stock_set.first(),
        fulfillment_id=fulfillment.pk,
    )
    variables = {
        "order": order_id,
        "input": {
            "notifyCustomer": True,
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 4, "warehouse": warehouse_id}],
                },
                {
                    "orderLineId": order_line2_id,
                    "stocks": [{"quantity": 2, "warehouse": warehouse_id}],
                },
            ],
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    error = data["errors"][0]
    assert error["field"] == "orderLineId"
    assert error["code"] == OrderErrorCode.FULFILL_ORDER_LINE.name

    mock_create_fulfillments.assert_not_called()


@patch("saleor.graphql.order.mutations.order_fulfill.create_fulfillments")
def test_order_fulfill_as_app(
    mock_create_fulfillments,
    app_api_client,
    order_with_lines,
    permission_manage_orders,
    warehouse,
    site_settings,
):
    order = order_with_lines
    query = ORDER_FULFILL_MUTATION
    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line, order_line2 = order.lines.all()
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    order_line2_id = graphene.Node.to_global_id("OrderLine", order_line2.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    variables = {
        "order": order_id,
        "input": {
            "notifyCustomer": True,
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 3, "warehouse": warehouse_id}],
                },
                {
                    "orderLineId": order_line2_id,
                    "stocks": [{"quantity": 2, "warehouse": warehouse_id}],
                },
            ],
        },
    }
    response = app_api_client.post_graphql(
        query, variables, permissions=(permission_manage_orders,)
    )
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert not data["errors"]

    fulfillment_lines_for_warehouses = {
        warehouse.pk: [
            {"order_line": order_line, "quantity": 3},
            {"order_line": order_line2, "quantity": 2},
        ]
    }
    mock_create_fulfillments.assert_called_once_with(
        None,
        app_api_client.app,
        order,
        fulfillment_lines_for_warehouses,
        ANY,
        site_settings,
        True,
        allow_stock_to_be_exceeded=False,
        approved=True,
        tracking_number="",
    )


@patch("saleor.graphql.order.mutations.order_fulfill.create_fulfillments")
def test_order_fulfill_many_warehouses(
    mock_create_fulfillments,
    staff_api_client,
    staff_user,
    order_with_lines,
    permission_group_manage_orders,
    warehouses,
    site_settings,
):
    order = order_with_lines
    query = ORDER_FULFILL_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)

    warehouse1, warehouse2 = warehouses
    order_line1, order_line2 = order.lines.all()

    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line1_id = graphene.Node.to_global_id("OrderLine", order_line1.id)
    order_line2_id = graphene.Node.to_global_id("OrderLine", order_line2.id)
    warehouse1_id = graphene.Node.to_global_id("Warehouse", warehouse1.pk)
    warehouse2_id = graphene.Node.to_global_id("Warehouse", warehouse2.pk)

    variables = {
        "order": order_id,
        "input": {
            "lines": [
                {
                    "orderLineId": order_line1_id,
                    "stocks": [{"quantity": 3, "warehouse": warehouse1_id}],
                },
                {
                    "orderLineId": order_line2_id,
                    "stocks": [
                        {"quantity": 1, "warehouse": warehouse1_id},
                        {"quantity": 1, "warehouse": warehouse2_id},
                    ],
                },
            ],
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert not data["errors"]

    fulfillment_lines_for_warehouses = {
        warehouse1.pk: [
            {"order_line": order_line1, "quantity": 3},
            {"order_line": order_line2, "quantity": 1},
        ],
        warehouse2.pk: [{"order_line": order_line2, "quantity": 1}],
    }

    mock_create_fulfillments.assert_called_once_with(
        staff_user,
        None,
        order,
        fulfillment_lines_for_warehouses,
        ANY,
        site_settings,
        True,
        allow_stock_to_be_exceeded=False,
        approved=True,
        tracking_number="",
    )


@patch("saleor.giftcard.utils.send_gift_card_notification")
def test_order_fulfill_with_gift_cards(
    mock_send_notification,
    staff_api_client,
    staff_user,
    order,
    gift_card_non_shippable_order_line,
    gift_card_shippable_order_line,
    permission_group_manage_orders,
    warehouse,
):
    query = ORDER_FULFILL_MUTATION
    order_id = graphene.Node.to_global_id("Order", order.id)
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order_line, order_line2 = (
        gift_card_non_shippable_order_line,
        gift_card_shippable_order_line,
    )
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    order_line2_id = graphene.Node.to_global_id("OrderLine", order_line2.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    variables = {
        "order": order_id,
        "input": {
            "notifyCustomer": True,
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 1, "warehouse": warehouse_id}],
                },
                {
                    "orderLineId": order_line2_id,
                    "stocks": [{"quantity": 1, "warehouse": warehouse_id}],
                },
            ],
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    flush_post_commit_hooks()
    data = content["data"]["orderFulfill"]
    assert not data["errors"]
    gift_cards = GiftCard.objects.all()
    assert gift_cards.count() == 2
    non_shippable_gift_card = gift_cards.get(
        product_id=gift_card_non_shippable_order_line.variant.product_id
    )
    shippable_gift_card = gift_cards.get(
        product_id=gift_card_shippable_order_line.variant.product_id
    )
    assert non_shippable_gift_card.initial_balance.amount == round(
        gift_card_non_shippable_order_line.unit_price_gross.amount, 2
    )
    assert non_shippable_gift_card.current_balance.amount == round(
        gift_card_non_shippable_order_line.unit_price_gross.amount, 2
    )
    assert non_shippable_gift_card.fulfillment_line
    assert shippable_gift_card.initial_balance.amount == round(
        gift_card_shippable_order_line.unit_price_gross.amount, 2
    )
    assert shippable_gift_card.current_balance.amount == round(
        gift_card_shippable_order_line.unit_price_gross.amount, 2
    )
    assert shippable_gift_card.fulfillment_line

    assert GiftCardEvent.objects.filter(
        gift_card=shippable_gift_card, type=GiftCardEvents.BOUGHT
    )
    assert GiftCardEvent.objects.filter(
        gift_card=non_shippable_gift_card, type=GiftCardEvents.BOUGHT
    )

    mock_send_notification.assert_called_once_with(
        staff_user,
        None,
        order.user,
        order.user_email,
        non_shippable_gift_card,
        ANY,
        order.channel.slug,
        resending=False,
    )


@patch("saleor.giftcard.utils.send_gift_card_notification")
def test_order_fulfill_with_gift_card_lines_waiting_for_approval(
    mock_send_notification,
    staff_api_client,
    staff_user,
    order,
    gift_card_non_shippable_order_line,
    gift_card_shippable_order_line,
    permission_group_manage_orders,
    warehouse,
    site_settings,
):
    query = ORDER_FULFILL_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)

    site_settings.fulfillment_auto_approve = False
    site_settings.save(update_fields=["fulfillment_auto_approve"])

    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line, order_line2 = (
        gift_card_non_shippable_order_line,
        gift_card_shippable_order_line,
    )
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    order_line2_id = graphene.Node.to_global_id("OrderLine", order_line2.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    quantity = 1
    variables = {
        "order": order_id,
        "input": {
            "notifyCustomer": True,
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": quantity, "warehouse": warehouse_id}],
                },
                {
                    "orderLineId": order_line2_id,
                    "stocks": [{"quantity": quantity, "warehouse": warehouse_id}],
                },
            ],
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert not data["errors"]
    # ensure gift card weren't created
    assert GiftCard.objects.count() == 0

    mock_send_notification.assert_not_called()


@patch("saleor.giftcard.utils.send_gift_card_notification")
def test_order_fulfill_with_gift_cards_by_app(
    mock_send_notification,
    app_api_client,
    order,
    gift_card_shippable_order_line,
    permission_manage_orders,
    warehouse,
    site_settings,
):
    query = ORDER_FULFILL_MUTATION
    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line = gift_card_shippable_order_line
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    quantity = 2
    variables = {
        "order": order_id,
        "input": {
            "notifyCustomer": True,
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": quantity, "warehouse": warehouse_id}],
                },
            ],
        },
    }
    response = app_api_client.post_graphql(
        query, variables, permissions=(permission_manage_orders,)
    )
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert not data["errors"]
    assert GiftCard.objects.count() == quantity

    mock_send_notification.assert_not_called


@patch("saleor.giftcard.utils.send_gift_card_notification")
def test_order_fulfill_with_gift_cards_multiple_warehouses(
    mock_send_notification,
    app_api_client,
    order,
    gift_card_shippable_order_line,
    permission_manage_orders,
    warehouses,
    shipping_zone,
    site_settings,
):
    query = ORDER_FULFILL_MUTATION
    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line = gift_card_shippable_order_line
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    warehouse1, warehouse2 = warehouses
    for warehouse in warehouses:
        warehouse.shipping_zones.add(shipping_zone)
        warehouse.save()
    stock_1 = Stock.objects.create(
        warehouse=warehouse1, product_variant=order_line.variant, quantity=1
    )
    Allocation.objects.create(
        order_line=order_line, stock=stock_1, quantity_allocated=1
    )
    stock_2 = Stock.objects.create(
        warehouse=warehouse2, product_variant=order_line.variant, quantity=1
    )
    Allocation.objects.create(
        order_line=order_line, stock=stock_2, quantity_allocated=1
    )
    warehouse1_id = graphene.Node.to_global_id("Warehouse", warehouse1.pk)
    warehouse2_id = graphene.Node.to_global_id("Warehouse", warehouse2.pk)
    quantity_1 = 2
    quantity_2 = 1
    variables = {
        "order": order_id,
        "input": {
            "notifyCustomer": True,
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [
                        {"quantity": quantity_1, "warehouse": warehouse1_id},
                        {"quantity": quantity_2, "warehouse": warehouse2_id},
                    ],
                },
            ],
        },
    }
    response = app_api_client.post_graphql(
        query, variables, permissions=(permission_manage_orders,)
    )
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert not data["errors"]
    assert GiftCard.objects.count() == quantity_1 + quantity_2

    mock_send_notification.assert_not_called


@patch("saleor.graphql.order.mutations.order_fulfill.create_fulfillments")
def test_order_fulfill_without_notification(
    mock_create_fulfillments,
    staff_api_client,
    staff_user,
    order_with_lines,
    permission_group_manage_orders,
    warehouse,
    site_settings,
):
    order = order_with_lines
    query = ORDER_FULFILL_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line = order.lines.first()
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    variables = {
        "order": order_id,
        "input": {
            "notifyCustomer": False,
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 1, "warehouse": warehouse_id}],
                }
            ],
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert not data["errors"]

    fulfillment_lines_for_warehouses = {
        warehouse.pk: [{"order_line": order_line, "quantity": 1}]
    }
    mock_create_fulfillments.assert_called_once_with(
        staff_user,
        None,
        order,
        fulfillment_lines_for_warehouses,
        ANY,
        site_settings,
        False,
        allow_stock_to_be_exceeded=False,
        approved=True,
        tracking_number="",
    )


@patch("saleor.graphql.order.mutations.order_fulfill.create_fulfillments")
def test_order_fulfill_lines_with_empty_quantity(
    mock_create_fulfillments,
    staff_api_client,
    staff_user,
    order_with_lines,
    permission_group_manage_orders,
    warehouse,
    warehouse_no_shipping_zone,
    site_settings,
):
    order = order_with_lines
    query = ORDER_FULFILL_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line, order_line2 = order.lines.all()
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    order_line2_id = graphene.Node.to_global_id("OrderLine", order_line2.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    warehouse2_id = graphene.Node.to_global_id(
        "Warehouse", warehouse_no_shipping_zone.pk
    )
    assert not order.events.all()
    variables = {
        "order": order_id,
        "input": {
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [
                        {"quantity": 0, "warehouse": warehouse_id},
                        {"quantity": 0, "warehouse": warehouse2_id},
                    ],
                },
                {
                    "orderLineId": order_line2_id,
                    "stocks": [
                        {"quantity": 2, "warehouse": warehouse_id},
                        {"quantity": 0, "warehouse": warehouse2_id},
                    ],
                },
            ],
        },
    }
    variables["input"]["lines"][0]["stocks"][0]["quantity"] = 0
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert not data["errors"]

    fulfillment_lines_for_warehouses = {
        warehouse.pk: [{"order_line": order_line2, "quantity": 2}]
    }
    mock_create_fulfillments.assert_called_once_with(
        staff_user,
        None,
        order,
        fulfillment_lines_for_warehouses,
        ANY,
        site_settings,
        True,
        allow_stock_to_be_exceeded=False,
        approved=True,
        tracking_number="",
    )


@pytest.mark.parametrize("fulfillment_auto_approve", [True, False])
@patch("saleor.graphql.order.mutations.order_fulfill.create_fulfillments")
def test_order_fulfill_without_sku(
    mock_create_fulfillments,
    fulfillment_auto_approve,
    staff_api_client,
    staff_user,
    order_with_lines,
    permission_group_manage_orders,
    warehouse,
    site_settings,
):
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    ProductVariant.objects.update(sku=None)
    site_settings.fulfillment_auto_approve = fulfillment_auto_approve
    site_settings.save(update_fields=["fulfillment_auto_approve"])
    order = order_with_lines
    query = ORDER_FULFILL_MUTATION
    order.lines.update(product_sku=None)
    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line, order_line2 = order.lines.all()
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    order_line2_id = graphene.Node.to_global_id("OrderLine", order_line2.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    variables = {
        "order": order_id,
        "input": {
            "notifyCustomer": True,
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 3, "warehouse": warehouse_id}],
                },
                {
                    "orderLineId": order_line2_id,
                    "stocks": [{"quantity": 2, "warehouse": warehouse_id}],
                },
            ],
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert not data["errors"]

    fulfillment_lines_for_warehouses = {
        warehouse.pk: [
            {"order_line": order_line, "quantity": 3},
            {"order_line": order_line2, "quantity": 2},
        ]
    }
    mock_create_fulfillments.assert_called_once_with(
        staff_user,
        None,
        order,
        fulfillment_lines_for_warehouses,
        ANY,
        site_settings,
        True,
        allow_stock_to_be_exceeded=False,
        approved=fulfillment_auto_approve,
        tracking_number="",
    )


@patch("saleor.graphql.order.mutations.order_fulfill.create_fulfillments")
def test_order_fulfill_zero_quantity(
    mock_create_fulfillments,
    staff_api_client,
    staff_user,
    order_with_lines,
    permission_group_manage_orders,
    warehouse,
):
    query = ORDER_FULFILL_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order_id = graphene.Node.to_global_id("Order", order_with_lines.id)
    order_line = order_with_lines.lines.first()
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    variables = {
        "order": order_id,
        "input": {
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 0, "warehouse": warehouse_id}],
                }
            ]
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert data["errors"]
    error = data["errors"][0]
    assert error["field"] == "lines"
    assert error["code"] == OrderErrorCode.ZERO_QUANTITY.name
    assert not error["orderLines"]
    assert not error["warehouse"]

    mock_create_fulfillments.assert_not_called()


def test_order_fulfill_channel_without_shipping_zones(
    staff_api_client,
    order_with_lines,
    permission_group_manage_orders,
    warehouse,
):
    order = order_with_lines
    order.channel.shipping_zones.clear()
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    query = ORDER_FULFILL_MUTATION
    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line = order.lines.first()
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    variables = {
        "order": order_id,
        "input": {
            "notifyCustomer": True,
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 3, "warehouse": warehouse_id}],
                },
            ],
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert len(data["errors"]) == 1
    error = data["errors"][0]
    assert error["field"] == "stocks"
    assert error["code"] == OrderErrorCode.INSUFFICIENT_STOCK.name


@patch("saleor.graphql.order.mutations.order_fulfill.create_fulfillments")
def test_order_fulfill_fulfilled_order(
    mock_create_fulfillments,
    staff_api_client,
    staff_user,
    order_with_lines,
    permission_group_manage_orders,
    warehouse,
):
    query = ORDER_FULFILL_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order_id = graphene.Node.to_global_id("Order", order_with_lines.id)
    order_line = order_with_lines.lines.first()
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    variables = {
        "order": order_id,
        "input": {
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 100, "warehouse": warehouse_id}],
                }
            ]
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert data["errors"]
    error = data["errors"][0]
    assert error["field"] == "orderLineId"
    assert error["code"] == OrderErrorCode.FULFILL_ORDER_LINE.name
    assert error["orderLines"] == [order_line_id]
    assert not error["warehouse"]

    mock_create_fulfillments.assert_not_called()


@patch("saleor.graphql.order.mutations.order_fulfill.create_fulfillments")
def test_order_fulfill_unpaid_order_and_disallow_unpaid(
    mock_create_fulfillments,
    staff_api_client,
    order_with_lines,
    permission_group_manage_orders,
    warehouse,
    site_settings,
):
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    site_settings.fulfillment_allow_unpaid = False
    site_settings.save(update_fields=["fulfillment_allow_unpaid"])
    query = ORDER_FULFILL_MUTATION
    order_id = graphene.Node.to_global_id("Order", order_with_lines.id)
    order_line = order_with_lines.lines.first()
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    variables = {
        "order": order_id,
        "input": {
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 100, "warehouse": warehouse_id}],
                }
            ]
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert data["errors"]
    error = data["errors"][0]
    assert error["field"] == "order"
    assert error["code"] == OrderErrorCode.CANNOT_FULFILL_UNPAID_ORDER.name

    mock_create_fulfillments.assert_not_called()


@patch(
    "saleor.graphql.order.mutations.order_fulfill.create_fulfillments", autospec=True
)
def test_order_fulfill_warehouse_with_insufficient_stock_exception(
    mock_create_fulfillments,
    staff_api_client,
    order_with_lines,
    permission_group_manage_orders,
    warehouse_no_shipping_zone,
):
    order = order_with_lines
    query = ORDER_FULFILL_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line = order.lines.first()
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    warehouse_id = graphene.Node.to_global_id(
        "Warehouse", warehouse_no_shipping_zone.pk
    )
    variables = {
        "order": order_id,
        "input": {
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 1, "warehouse": warehouse_id}],
                }
            ]
        },
    }

    mock_create_fulfillments.side_effect = InsufficientStock(
        [
            InsufficientStockData(
                variant=order_line.variant,
                order_line=order_line,
                warehouse_pk=warehouse_no_shipping_zone.pk,
                available_quantity=0,
            )
        ]
    )

    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert data["errors"]
    error = data["errors"][0]
    assert error["field"] == "stocks"
    assert error["code"] == OrderErrorCode.INSUFFICIENT_STOCK.name
    assert error["orderLines"] == [order_line_id]
    assert error["warehouse"] == warehouse_id


@patch(
    "saleor.graphql.order.mutations.order_fulfill.create_fulfillments", autospec=True
)
def test_order_fulfill_warehouse_duplicated_warehouse_id(
    mock_create_fulfillments,
    staff_api_client,
    order_with_lines,
    permission_group_manage_orders,
    warehouse,
):
    order = order_with_lines
    query = ORDER_FULFILL_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line = order.lines.first()
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    variables = {
        "order": order_id,
        "input": {
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [
                        {"quantity": 1, "warehouse": warehouse_id},
                        {"quantity": 2, "warehouse": warehouse_id},
                    ],
                }
            ]
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert data["errors"]
    error = data["errors"][0]
    assert error["field"] == "warehouse"
    assert error["code"] == OrderErrorCode.DUPLICATED_INPUT_ITEM.name
    assert not error["orderLines"]
    assert error["warehouse"] == warehouse_id
    mock_create_fulfillments.assert_not_called()


@patch(
    "saleor.graphql.order.mutations.order_fulfill.create_fulfillments", autospec=True
)
def test_order_fulfill_warehouse_duplicated_order_line_id(
    mock_create_fulfillments,
    staff_api_client,
    order_with_lines,
    permission_group_manage_orders,
    warehouse,
):
    order = order_with_lines
    query = ORDER_FULFILL_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line = order.lines.first()
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    variables = {
        "order": order_id,
        "input": {
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 3, "warehouse": warehouse_id}],
                },
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 3, "warehouse": warehouse_id}],
                },
            ]
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert data["errors"]
    error = data["errors"][0]
    assert error["field"] == "orderLineId"
    assert error["code"] == OrderErrorCode.DUPLICATED_INPUT_ITEM.name
    assert error["orderLines"] == [order_line_id]
    assert not error["warehouse"]
    mock_create_fulfillments.assert_not_called()


@patch("saleor.graphql.order.mutations.order_fulfill.create_fulfillments")
def test_order_fulfill_preorder(
    mock_create_fulfillments,
    staff_api_client,
    staff_user,
    order_with_lines,
    permission_group_manage_orders,
    warehouse,
):
    query = ORDER_FULFILL_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order_id = graphene.Node.to_global_id("Order", order_with_lines.id)
    order_line = order_with_lines.lines.first()
    variant = order_line.variant
    variant.is_preorder = True
    variant.save(update_fields=["is_preorder"])

    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    variables = {
        "order": order_id,
        "input": {
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 0, "warehouse": warehouse_id}],
                }
            ]
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert data["errors"]
    error = data["errors"][0]
    assert error["field"] == "orderLineId"
    assert error["code"] == OrderErrorCode.FULFILL_ORDER_LINE.name
    assert error["orderLines"]

    mock_create_fulfillments.assert_not_called()


def test_order_fulfill_preorder_waiting_fulfillment(
    staff_api_client,
    order_with_lines,
    permission_group_manage_orders,
    warehouse,
    site_settings,
):
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    site_settings.fulfillment_auto_approve = False
    site_settings.save(update_fields=["fulfillment_auto_approve"])
    query = ORDER_FULFILL_MUTATION
    order_id = graphene.Node.to_global_id("Order", order_with_lines.id)
    order_line = order_with_lines.lines.first()
    variant = order_line.variant
    variant.is_preorder = True
    variant.save(update_fields=["is_preorder"])

    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    variables = {
        "order": order_id,
        "input": {
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 3, "warehouse": warehouse_id}],
                }
            ]
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    content = get_graphql_content(response)
    data = content["data"]["orderFulfill"]
    assert not data["errors"]
    assert (
        order_with_lines.fulfillments.first().status
        == FulfillmentStatus.WAITING_FOR_APPROVAL
    )


@patch("saleor.order.actions.send_fulfillment_confirmation_to_customer", autospec=True)
def test_create_digital_fulfillment(
    mock_email_fulfillment,
    digital_content,
    staff_api_client,
    order_with_lines,
    warehouse,
    permission_group_manage_orders,
):
    order = order_with_lines
    query = ORDER_FULFILL_MUTATION
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line = order.lines.first()
    order_line.variant = digital_content.product_variant
    order_line.save()
    order_line.allocations.all().delete()

    stock = digital_content.product_variant.stocks.get(warehouse=warehouse)
    Allocation.objects.create(
        order_line=order_line, stock=stock, quantity_allocated=order_line.quantity
    )

    second_line = order.lines.last()
    first_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    second_line_id = graphene.Node.to_global_id("OrderLine", second_line.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)

    variables = {
        "order": order_id,
        "input": {
            "notifyCustomer": True,
            "lines": [
                {
                    "orderLineId": first_line_id,
                    "stocks": [{"quantity": 1, "warehouse": warehouse_id}],
                },
                {
                    "orderLineId": second_line_id,
                    "stocks": [{"quantity": 1, "warehouse": warehouse_id}],
                },
            ],
        },
    }
    response = staff_api_client.post_graphql(query, variables)
    get_graphql_content(response)

    assert mock_email_fulfillment.call_count == 1


<<<<<<< HEAD:saleor/graphql/order/tests/test_fulfillment.py
APPROVE_FULFILLMENT_MUTATION = """
    mutation approveFulfillment(
        $id: ID!, $notifyCustomer: Boolean!, $allowStockToBeExceeded: Boolean = false
    ) {
        orderFulfillmentApprove(
                id: $id,
                notifyCustomer: $notifyCustomer,
                allowStockToBeExceeded: $allowStockToBeExceeded) {
            fulfillment {
                status
            }
            order {
                status
            }
            errors {
                field
                code
                message
            }
        }
    }
"""


@patch("saleor.plugins.manager.PluginsManager.fulfillment_approved")
@patch("saleor.order.actions.send_fulfillment_confirmation_to_customer", autospec=True)
def test_fulfillment_approve(
    mock_email_fulfillment,
    mock_fulfillment_approved,
    staff_api_client,
    fulfillment,
    permission_manage_orders,
):
    fulfillment.status = FulfillmentStatus.WAITING_FOR_APPROVAL
    fulfillment.save(update_fields=["status"])
    query = APPROVE_FULFILLMENT_MUTATION
    fulfillment_id = graphene.Node.to_global_id("Fulfillment", fulfillment.id)
    variables = {"id": fulfillment_id, "notifyCustomer": True}
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_orders]
    )
    content = get_graphql_content(response)
    data = content["data"]["orderFulfillmentApprove"]
    assert not data["errors"]
    assert data["fulfillment"]["status"] == FulfillmentStatus.FULFILLED.upper()
    assert data["order"]["status"] == OrderStatus.FULFILLED.upper()
    fulfillment.refresh_from_db()
    assert fulfillment.status == FulfillmentStatus.FULFILLED

    assert mock_email_fulfillment.call_count == 1
    events = fulfillment.order.events.all()
    assert len(events) == 1
    event = events[0]
    assert event.type == OrderEvents.FULFILLMENT_FULFILLED_ITEMS
    assert event.user == staff_api_client.user
    mock_fulfillment_approved.assert_called_once_with(fulfillment)


@patch("saleor.order.actions.send_fulfillment_confirmation_to_customer", autospec=True)
def test_fulfillment_approve_delete_products_before_approval_allow_stock_exceeded_true(
    mock_email_fulfillment,
    staff_api_client,
    fulfillment,
    permission_manage_orders,
):
    fulfillment.status = FulfillmentStatus.WAITING_FOR_APPROVAL
    fulfillment.save(update_fields=["status"])

    Product.objects.all().delete()

    query = APPROVE_FULFILLMENT_MUTATION
    fulfillment_id = graphene.Node.to_global_id("Fulfillment", fulfillment.id)
    variables = {
        "id": fulfillment_id,
        "notifyCustomer": True,
        "allowStockToBeExceeded": True,
    }
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_orders]
    )
    content = get_graphql_content(response)
    data = content["data"]["orderFulfillmentApprove"]
    assert not data["errors"]
    assert data["fulfillment"]["status"] == FulfillmentStatus.FULFILLED.upper()
    assert data["order"]["status"] == OrderStatus.FULFILLED.upper()
    fulfillment.refresh_from_db()
    assert fulfillment.status == FulfillmentStatus.FULFILLED

    assert mock_email_fulfillment.call_count == 1
    events = fulfillment.order.events.all()
    assert len(events) == 1
    event = events[0]
    assert event.type == OrderEvents.FULFILLMENT_FULFILLED_ITEMS
    assert event.user == staff_api_client.user


@patch("saleor.plugins.manager.PluginsManager.fulfillment_approved")
@patch("saleor.order.actions.send_fulfillment_confirmation_to_customer", autospec=True)
def test_fulfillment_approve_delete_products_before_approval_allow_stock_exceeded_false(
    mock_email_fulfillment,
    mock_fulfillment_approved,
    staff_api_client,
    fulfillment,
    permission_manage_orders,
):
    fulfillment.status = FulfillmentStatus.WAITING_FOR_APPROVAL
    fulfillment.save(update_fields=["status"])

    Product.objects.all().delete()

    query = APPROVE_FULFILLMENT_MUTATION
    fulfillment_id = graphene.Node.to_global_id("Fulfillment", fulfillment.id)
    variables = {
        "id": fulfillment_id,
        "notifyCustomer": True,
        "allowStockToBeExceeded": False,
    }
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_orders]
    )

    content = get_graphql_content(response)
    errors = content["data"]["orderFulfillmentApprove"]["errors"]

    assert len(errors) == 2

    error_field_and_code = {
        "field": "stocks",
        "code": "INSUFFICIENT_STOCK",
    }
    expected_errors = [
        {
            **error_field_and_code,
            "message": f"Insufficient product stock: {line.order_line}",
        }
        for line in fulfillment.lines.all()
    ]

    for expected_error in expected_errors:
        assert expected_error in errors

    fulfillment.refresh_from_db()
    assert fulfillment.status == FulfillmentStatus.WAITING_FOR_APPROVAL

    assert mock_email_fulfillment.call_count == 1
    events = fulfillment.order.events.all()
    assert len(events) == 0
    mock_fulfillment_approved.assert_not_called()


@patch("saleor.order.actions.send_fulfillment_confirmation_to_customer", autospec=True)
def test_fulfillment_approve_gift_cards_created(
    mock_email_fulfillment,
    staff_api_client,
    fulfillment,
    permission_manage_orders,
    gift_card_shippable_order_line,
    gift_card_non_shippable_order_line,
):
    fulfillment.status = FulfillmentStatus.WAITING_FOR_APPROVAL
    fulfillment.save(update_fields=["status"])

    gift_card_line_1 = gift_card_shippable_order_line
    gift_card_line_2 = gift_card_non_shippable_order_line
    stock_1 = gift_card_line_1.variant.stocks.first()
    stock_2 = gift_card_line_2.variant.stocks.first()
    fulfillment_line_1 = fulfillment.lines.create(
        order_line=gift_card_line_1, quantity=gift_card_line_1.quantity, stock=stock_1
    )
    fulfillment_line_2 = fulfillment.lines.create(
        order_line=gift_card_line_2, quantity=gift_card_line_2.quantity, stock=stock_2
    )

    fulfill_order_lines(
        [
            OrderLineInfo(
                line=gift_card_line_1,
                quantity=gift_card_line_1.quantity,
                warehouse_pk=stock_1.warehouse.pk,
            ),
            OrderLineInfo(
                line=gift_card_line_2,
                quantity=gift_card_line_2.quantity,
                warehouse_pk=stock_2.warehouse.pk,
            ),
        ],
        manager=get_plugins_manager(),
    )

    query = APPROVE_FULFILLMENT_MUTATION
    fulfillment_id = graphene.Node.to_global_id("Fulfillment", fulfillment.id)
    variables = {"id": fulfillment_id, "notifyCustomer": True}
    assert GiftCard.objects.count() == 0

    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_orders]
    )
    content = get_graphql_content(response)
    data = content["data"]["orderFulfillmentApprove"]
    assert not data["errors"]
    assert data["fulfillment"]["status"] == FulfillmentStatus.FULFILLED.upper()
    assert data["order"]["status"] == OrderStatus.FULFILLED.upper()
    fulfillment.refresh_from_db()
    assert fulfillment.status == FulfillmentStatus.FULFILLED

    assert mock_email_fulfillment.call_count == 1
    events = fulfillment.order.events.all()
    assert len(events) == 1
    event = events[0]
    assert event.type == OrderEvents.FULFILLMENT_FULFILLED_ITEMS
    assert event.user == staff_api_client.user
    gift_cards = GiftCard.objects.all()
    assert gift_cards.count() == gift_card_line_1.quantity + gift_card_line_2.quantity
    for gift_card in gift_cards:
        if gift_card.product == gift_card_line_1.variant.product:
            assert gift_card.fulfillment_line == fulfillment_line_1
        else:
            assert gift_card.fulfillment_line == fulfillment_line_2


@patch("saleor.order.actions.send_fulfillment_confirmation_to_customer", autospec=True)
def test_fulfillment_approve_when_stock_is_exceeded_and_flag_enabled(
    mock_email_fulfillment,
    staff_api_client,
    fulfillment,
    permission_manage_orders,
):
    # make stocks exceeded
    for stock in [line.stock for line in fulfillment.lines.all()]:
        stock.quantity = -99
        stock.save()

    fulfillment.status = FulfillmentStatus.WAITING_FOR_APPROVAL
    fulfillment.save(update_fields=["status"])
    query = APPROVE_FULFILLMENT_MUTATION
    fulfillment_id = graphene.Node.to_global_id("Fulfillment", fulfillment.id)

    # make response with flag disabled, raised error is expected
    variables = {
        "id": fulfillment_id,
        "notifyCustomer": True,
        "allowStockToBeExceeded": True,
    }
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_orders]
    )
    content = get_graphql_content(response)
    data = content["data"]["orderFulfillmentApprove"]
    assert not data["errors"]
    assert data["fulfillment"]["status"] == FulfillmentStatus.FULFILLED.upper()
    assert data["order"]["status"] == OrderStatus.FULFILLED.upper()
    fulfillment.refresh_from_db()
    assert fulfillment.status == FulfillmentStatus.FULFILLED

    assert mock_email_fulfillment.call_count == 1
    events = fulfillment.order.events.all()
    assert len(events) == 1
    event = events[0]
    assert event.type == OrderEvents.FULFILLMENT_FULFILLED_ITEMS
    assert event.user == staff_api_client.user


@patch("saleor.order.actions.send_fulfillment_confirmation_to_customer", autospec=True)
def test_fulfillment_approve_when_stock_is_exceeded_and_flag_disabled(
    mock_email_fulfillment,
    staff_api_client,
    fulfillment,
    permission_manage_orders,
):
    # make stocks exceeded
    for stock in [line.stock for line in fulfillment.lines.all()]:
        stock.quantity = -99
        stock.save()

    fulfillment.status = FulfillmentStatus.WAITING_FOR_APPROVAL
    fulfillment.save(update_fields=["status"])
    query = APPROVE_FULFILLMENT_MUTATION
    fulfillment_id = graphene.Node.to_global_id("Fulfillment", fulfillment.id)

    variables = {
        "id": fulfillment_id,
        "notifyCustomer": True,
        "allowStockToBeExceeded": False,
    }
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_orders]
    )
    content = get_graphql_content(response, ignore_errors=True)
    errors = content["data"]["orderFulfillmentApprove"]["errors"]

    assert len(errors) == 2

    error_field_and_code = {
        "field": "stocks",
        "code": "INSUFFICIENT_STOCK",
    }

    expected_errors = [
        {
            **error_field_and_code,
            "message": f"Insufficient product stock: {line.order_line}",
        }
        for line in fulfillment.lines.all()
    ]

    for expected_error in expected_errors:
        assert expected_error in errors


@patch("saleor.order.actions.send_fulfillment_confirmation_to_customer", autospec=True)
def test_fulfillment_approve_partial_order_fulfill(
    mock_email_fulfillment,
    staff_api_client,
    fulfillment_awaiting_approval,
    permission_manage_orders,
):
    # given
    query = APPROVE_FULFILLMENT_MUTATION
    order = fulfillment_awaiting_approval.order

    second_fulfillment = order.fulfillments.create()
    line_1 = order.lines.first()
    line_2 = order.lines.last()
    second_fulfillment.lines.create(
        order_line=line_1, quantity=line_1.quantity - line_1.quantity_fulfilled
    )
    second_fulfillment.lines.create(
        order_line=line_2, quantity=line_2.quantity - line_2.quantity_fulfilled
    )
    second_fulfillment.status = FulfillmentStatus.WAITING_FOR_APPROVAL
    second_fulfillment.save()

    line_1.quantity_fulfilled = line_1.quantity
    line_2.quantity_fulfilled = line_2.quantity

    OrderLine.objects.bulk_update([line_1, line_2], ["quantity_fulfilled"])

    fulfillment_id = graphene.Node.to_global_id(
        "Fulfillment", fulfillment_awaiting_approval.id
    )
    variables = {"id": fulfillment_id, "notifyCustomer": False}

    # when
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_orders]
    )

    # then
    content = get_graphql_content(response)
    data = content["data"]["orderFulfillmentApprove"]
    assert not data["errors"]
    assert data["fulfillment"]["status"] == FulfillmentStatus.FULFILLED.upper()
    assert data["order"]["status"] == "PARTIALLY_FULFILLED"
    fulfillment_awaiting_approval.refresh_from_db()
    assert fulfillment_awaiting_approval.status == FulfillmentStatus.FULFILLED

    assert mock_email_fulfillment.call_count == 0


def test_fulfillment_approve_invalid_status(
    staff_api_client,
    fulfillment,
    permission_manage_orders,
):
    query = APPROVE_FULFILLMENT_MUTATION
    fulfillment_id = graphene.Node.to_global_id("Fulfillment", fulfillment.id)
    variables = {"id": fulfillment_id, "notifyCustomer": True}
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_orders]
    )
    content = get_graphql_content(response)
    data = content["data"]["orderFulfillmentApprove"]
    assert data["errors"][0]["code"] == OrderErrorCode.INVALID.name


def test_fulfillment_approve_order_unpaid(
    staff_api_client,
    fulfillment,
    site_settings,
    permission_manage_orders,
):
    site_settings.fulfillment_allow_unpaid = False
    site_settings.save(update_fields=["fulfillment_allow_unpaid"])
    fulfillment.status = FulfillmentStatus.WAITING_FOR_APPROVAL
    fulfillment.save(update_fields=["status"])
    query = APPROVE_FULFILLMENT_MUTATION
    fulfillment_id = graphene.Node.to_global_id("Fulfillment", fulfillment.id)
    variables = {"id": fulfillment_id, "notifyCustomer": True}
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_orders]
    )
    content = get_graphql_content(response)
    data = content["data"]["orderFulfillmentApprove"]
    assert data["errors"][0]["code"] == OrderErrorCode.CANNOT_FULFILL_UNPAID_ORDER.name


def test_fulfillment_approve_preorder(
    staff_api_client, fulfillment, permission_manage_orders, site_settings
):
    """Fulfillment with WAITING_FOR_APPROVAL status can not be fulfilled
    if it contains variant in preorder."""
    site_settings.fulfillment_auto_approve = False
    site_settings.save(update_fields=["fulfillment_auto_approve"])

    order_line = fulfillment.order.lines.first()
    variant = order_line.variant
    variant.is_preorder = True
    variant.save(update_fields=["is_preorder"])
    fulfillment.status = FulfillmentStatus.WAITING_FOR_APPROVAL
    fulfillment.save(update_fields=["status"])
    query = APPROVE_FULFILLMENT_MUTATION

    fulfillment_id = graphene.Node.to_global_id("Fulfillment", fulfillment.id)
    variables = {"id": fulfillment_id, "notifyCustomer": False}
    response = staff_api_client.post_graphql(
        query, variables, permissions=[permission_manage_orders]
    )
    content = get_graphql_content(response)
    data = content["data"]["orderFulfillmentApprove"]
    assert data["errors"]

    error = data["errors"][0]
    assert error["field"] == "orderLineId"
    assert error["code"] == OrderErrorCode.FULFILL_ORDER_LINE.name


QUERY_FULFILLMENT = """
    query fulfillment($id: ID!) {
        order(id: $id) {
            fulfillments {
                id
                fulfillmentOrder
                status
                trackingNumber
                warehouse {
                    id
                }
                lines {
                    orderLine {
                        id
                    }
                    quantity
                }
            }
        }
    }
"""


def test_fulfillment_query(
    staff_api_client,
    fulfilled_order,
=======
@patch("saleor.plugins.webhook.plugin.trigger_webhooks_async")
def test_order_fulfill_tracking_number_updated_event_triggered(
    mocked_webhooks,
    any_webhook,
    subscription_fulfillment_tracking_number_updated,
    subscription_fulfillment_created_webhook,
    staff_api_client,
    staff_user,
    order_with_lines,
    permission_group_manage_orders,
>>>>>>> fa9ea3af1251eaa792bebc0aabcf03f49b31a7e9:saleor/graphql/order/tests/mutations/test_order_fulfill.py
    warehouse,
    site_settings,
    settings,
):
    # given
    settings.PLUGINS = ["saleor.plugins.webhook.plugin.WebhookPlugin"]
    permission_group_manage_orders.user_set.add(staff_api_client.user)
    site_settings.fulfillment_auto_approve = True
    site_settings.save(update_fields=["fulfillment_auto_approve"])
    order = order_with_lines
    query = ORDER_FULFILL_MUTATION
    order_id = graphene.Node.to_global_id("Order", order.id)
    order_line, order_line2 = order.lines.all()
    order_line_id = graphene.Node.to_global_id("OrderLine", order_line.id)
    order_line2_id = graphene.Node.to_global_id("OrderLine", order_line2.id)
    warehouse_id = graphene.Node.to_global_id("Warehouse", warehouse.pk)
    variables = {
        "order": order_id,
        "input": {
            "notifyCustomer": True,
            "lines": [
                {
                    "orderLineId": order_line_id,
                    "stocks": [{"quantity": 3, "warehouse": warehouse_id}],
                },
                {
                    "orderLineId": order_line2_id,
                    "stocks": [{"quantity": 2, "warehouse": warehouse_id}],
                },
            ],
            "trackingNumber": "test_tracking_number",
        },
    }
    # when
    staff_api_client.post_graphql(query, variables)
    flush_post_commit_hooks()

    # then
    assert mocked_webhooks.call_count == 2
    mocked_tracking_updated = mocked_webhooks.call_args_list[0]
    mocked_fulfillment_created = mocked_webhooks.call_args_list[1]

    assert (
        mocked_tracking_updated[0][1]
        == WebhookEventAsyncType.FULFILLMENT_TRACKING_NUMBER_UPDATED
    )
    assert mocked_fulfillment_created[0][1] == WebhookEventAsyncType.FULFILLMENT_CREATED
