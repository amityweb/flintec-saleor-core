from typing import Any, Optional

from ..permission.enums import (
    AccountPermissions,
    AppPermission,
    BasePermissionEnum,
    ChannelPermissions,
    CheckoutPermissions,
    DiscountPermissions,
    GiftcardPermissions,
    MenuPermissions,
    OrderPermissions,
    PagePermissions,
    PageTypePermissions,
    PaymentPermissions,
    ProductPermissions,
    ShippingPermissions,
    SitePermissions,
)


class WebhookEventAsyncType:
    ANY = "any_events"

    ACCOUNT_CONFIRMATION_REQUESTED = "account_confirmation_requested"
    ACCOUNT_EMAIL_CHANGED = "account_email_changed"
    ACCOUNT_CHANGE_EMAIL_REQUESTED = "account_change_email_requested"
    ACCOUNT_SET_PASSWORD_REQUESTED = "account_set_password_requested"
    ACCOUNT_CONFIRMED = "account_confirmed"
    ACCOUNT_DELETE_REQUESTED = "account_delete_requested"
    ACCOUNT_DELETED = "account_deleted"

    ADDRESS_CREATED = "address_created"
    ADDRESS_UPDATED = "address_updated"
    ADDRESS_DELETED = "address_deleted"

    APP_INSTALLED = "app_installed"
    APP_UPDATED = "app_updated"
    APP_DELETED = "app_deleted"
    APP_STATUS_CHANGED = "app_status_changed"

    ATTRIBUTE_CREATED = "attribute_created"
    ATTRIBUTE_UPDATED = "attribute_updated"
    ATTRIBUTE_DELETED = "attribute_deleted"

    ATTRIBUTE_VALUE_CREATED = "attribute_value_created"
    ATTRIBUTE_VALUE_UPDATED = "attribute_value_updated"
    ATTRIBUTE_VALUE_DELETED = "attribute_value_deleted"

    CATEGORY_CREATED = "category_created"
    CATEGORY_UPDATED = "category_updated"
    CATEGORY_DELETED = "category_deleted"

    CHANNEL_CREATED = "channel_created"
    CHANNEL_UPDATED = "channel_updated"
    CHANNEL_DELETED = "channel_deleted"
    CHANNEL_STATUS_CHANGED = "channel_status_changed"
    CHANNEL_METADATA_UPDATED = "channel_metadata_updated"

    GIFT_CARD_CREATED = "gift_card_created"
    GIFT_CARD_UPDATED = "gift_card_updated"
    GIFT_CARD_DELETED = "gift_card_deleted"
    GIFT_CARD_SENT = "gift_card_sent"
    GIFT_CARD_STATUS_CHANGED = "gift_card_status_changed"
    GIFT_CARD_METADATA_UPDATED = "gift_card_metadata_updated"
    GIFT_CARD_EXPORT_COMPLETED = "gift_card_export_completed"

    MENU_CREATED = "menu_created"
    MENU_UPDATED = "menu_updated"
    MENU_DELETED = "menu_deleted"
    MENU_ITEM_CREATED = "menu_item_created"
    MENU_ITEM_UPDATED = "menu_item_updated"
    MENU_ITEM_DELETED = "menu_item_deleted"

    ORDER_CREATED = "order_created"
    ORDER_CONFIRMED = "order_confirmed"
    ORDER_PAID = "order_paid"
    ORDER_FULLY_PAID = "order_fully_paid"
    ORDER_REFUNDED = "order_refunded"
    ORDER_FULLY_REFUNDED = "order_fully_refunded"
    ORDER_UPDATED = "order_updated"
    ORDER_CANCELLED = "order_cancelled"
<<<<<<< HEAD
=======
    ORDER_EXPIRED = "order_expired"
>>>>>>> fa9ea3af1251eaa792bebc0aabcf03f49b31a7e9
    ORDER_FULFILLED = "order_fulfilled"
    ORDER_METADATA_UPDATED = "order_metadata_updated"
    ORDER_BULK_CREATED = "order_bulk_created"

    FULFILLMENT_CREATED = "fulfillment_created"
    FULFILLMENT_CANCELED = "fulfillment_canceled"
    FULFILLMENT_APPROVED = "fulfillment_approved"
    FULFILLMENT_METADATA_UPDATED = "fulfillment_metadata_updated"
    FULFILLMENT_TRACKING_NUMBER_UPDATED = "fulfillment_tracking_number_updated"

    FULFILLMENT_CREATED = "fulfillment_created"
    FULFILLMENT_CANCELED = "fulfillment_canceled"
    FULFILLMENT_APPROVED = "fulfillment_approved"

    DRAFT_ORDER_CREATED = "draft_order_created"
    DRAFT_ORDER_UPDATED = "draft_order_updated"
    DRAFT_ORDER_DELETED = "draft_order_deleted"

    SALE_CREATED = "sale_created"
    SALE_UPDATED = "sale_updated"
    SALE_DELETED = "sale_deleted"
    SALE_TOGGLE = "sale_toggle"

    PROMOTION_CREATED = "promotion_created"
    PROMOTION_UPDATED = "promotion_updated"
    PROMOTION_DELETED = "promotion_deleted"
    PROMOTION_STARTED = "promotion_started"
    PROMOTION_ENDED = "promotion_ended"

    PROMOTION_RULE_CREATED = "promotion_rule_created"
    PROMOTION_RULE_UPDATED = "promotion_rule_updated"
    PROMOTION_RULE_DELETED = "promotion_rule_deleted"

    INVOICE_REQUESTED = "invoice_requested"
    INVOICE_DELETED = "invoice_deleted"
    INVOICE_SENT = "invoice_sent"

    CUSTOMER_CREATED = "customer_created"
    CUSTOMER_UPDATED = "customer_updated"
    CUSTOMER_DELETED = "customer_deleted"
    CUSTOMER_METADATA_UPDATED = "customer_metadata_updated"

    COLLECTION_CREATED = "collection_created"
    COLLECTION_UPDATED = "collection_updated"
    COLLECTION_DELETED = "collection_deleted"
    COLLECTION_METADATA_UPDATED = "collection_metadata_updated"

    PRODUCT_CREATED = "product_created"
    PRODUCT_UPDATED = "product_updated"
    PRODUCT_DELETED = "product_deleted"
    PRODUCT_METADATA_UPDATED = "product_metadata_updated"
    PRODUCT_EXPORT_COMPLETED = "product_export_completed"

    PRODUCT_MEDIA_CREATED = "product_media_created"
    PRODUCT_MEDIA_UPDATED = "product_media_updated"
    PRODUCT_MEDIA_DELETED = "product_media_deleted"

    PRODUCT_VARIANT_CREATED = "product_variant_created"
    PRODUCT_VARIANT_UPDATED = "product_variant_updated"
    PRODUCT_VARIANT_DELETED = "product_variant_deleted"
    PRODUCT_VARIANT_METADATA_UPDATED = "product_variant_metadata_updated"

    PRODUCT_VARIANT_OUT_OF_STOCK = "product_variant_out_of_stock"
    PRODUCT_VARIANT_BACK_IN_STOCK = "product_variant_back_in_stock"
    PRODUCT_VARIANT_STOCK_UPDATED = "product_variant_stock_updated"

    CHECKOUT_CREATED = "checkout_created"
    CHECKOUT_UPDATED = "checkout_updated"
    CHECKOUT_FULLY_PAID = "checkout_fully_paid"
    CHECKOUT_METADATA_UPDATED = "checkout_metadata_updated"

    NOTIFY_USER = "notify_user"  # deprecated

    PAGE_CREATED = "page_created"
    PAGE_UPDATED = "page_updated"
    PAGE_DELETED = "page_deleted"

    PAGE_TYPE_CREATED = "page_type_created"
    PAGE_TYPE_UPDATED = "page_type_updated"
    PAGE_TYPE_DELETED = "page_type_deleted"

    PERMISSION_GROUP_CREATED = "permission_group_created"
    PERMISSION_GROUP_UPDATED = "permission_group_updated"
    PERMISSION_GROUP_DELETED = "permission_group_deleted"

    SHIPPING_PRICE_CREATED = "shipping_price_created"
    SHIPPING_PRICE_UPDATED = "shipping_price_updated"
    SHIPPING_PRICE_DELETED = "shipping_price_deleted"

    SHIPPING_ZONE_CREATED = "shipping_zone_created"
    SHIPPING_ZONE_UPDATED = "shipping_zone_updated"
    SHIPPING_ZONE_DELETED = "shipping_zone_deleted"
    SHIPPING_ZONE_METADATA_UPDATED = "shipping_zone_metadata_updated"

    STAFF_CREATED = "staff_created"
    STAFF_UPDATED = "staff_updated"
    STAFF_DELETED = "staff_deleted"
    STAFF_SET_PASSWORD_REQUESTED = "staff_set_password_requested"

    TRANSACTION_ITEM_METADATA_UPDATED = "transaction_item_metadata_updated"

    TRANSLATION_CREATED = "translation_created"
    TRANSLATION_UPDATED = "translation_updated"

    WAREHOUSE_CREATED = "warehouse_created"
    WAREHOUSE_UPDATED = "warehouse_updated"
    WAREHOUSE_DELETED = "warehouse_deleted"
    WAREHOUSE_METADATA_UPDATED = "warehouse_metadata_updated"

    VOUCHER_CREATED = "voucher_created"
    VOUCHER_UPDATED = "voucher_updated"
    VOUCHER_DELETED = "voucher_deleted"
    VOUCHER_CODES_CREATED = "voucher_codes_created"
    VOUCHER_CODES_DELETED = "voucher_codes_deleted"
    VOUCHER_METADATA_UPDATED = "voucher_metadata_updated"
    VOUCHER_CODE_EXPORT_COMPLETED = "voucher_code_export_completed"

    OBSERVABILITY = "observability"

<<<<<<< HEAD
    DISPLAY_LABELS = {
        ANY: "Any events",
        ADDRESS_CREATED: "Address created",
        ADDRESS_UPDATED: "Address updated",
        ADDRESS_DELETED: "Address deleted",
        APP_INSTALLED: "App created",
        APP_UPDATED: "App updated",
        APP_DELETED: "App deleted",
        APP_STATUS_CHANGED: "App status changed",
        ATTRIBUTE_CREATED: "Attribute created",
        ATTRIBUTE_UPDATED: "Attribute updated",
        ATTRIBUTE_DELETED: "Attribute deleted",
        ATTRIBUTE_VALUE_CREATED: "Attribute value created",
        ATTRIBUTE_VALUE_UPDATED: "Attribute value updated",
        ATTRIBUTE_VALUE_DELETED: "Attribute value deleted",
        CATEGORY_CREATED: "Category created",
        CATEGORY_UPDATED: "Category updated",
        CATEGORY_DELETED: "Category deleted",
        CHANNEL_CREATED: "Channel created",
        CHANNEL_UPDATED: "Channel updated",
        CHANNEL_DELETED: "Channel deleted",
        CHANNEL_STATUS_CHANGED: "Channel status changed",
        GIFT_CARD_CREATED: "Gift card created",
        GIFT_CARD_UPDATED: "Gift card updated",
        GIFT_CARD_DELETED: "Gift card deleted",
        GIFT_CARD_STATUS_CHANGED: "Gift card status changed",
        MENU_CREATED: "Menu created",
        MENU_UPDATED: "Menu updated",
        MENU_DELETED: "Menu deleted",
        MENU_ITEM_CREATED: "Menu item created",
        MENU_ITEM_UPDATED: "Menu item updated",
        MENU_ITEM_DELETED: "Menu item deleted",
        ORDER_CREATED: "Order created",
        ORDER_CONFIRMED: "Order confirmed",
        ORDER_FULLY_PAID: "Order paid",
        ORDER_UPDATED: "Order updated",
        ORDER_CANCELLED: "Order cancelled",
        ORDER_FULFILLED: "Order fulfilled",
        DRAFT_ORDER_CREATED: "Draft order created",
        DRAFT_ORDER_UPDATED: "Draft order updated",
        DRAFT_ORDER_DELETED: "Draft order deleted",
        SALE_CREATED: "Sale created",
        SALE_UPDATED: "Sale updated",
        SALE_DELETED: "Sale deleted",
        SALE_TOGGLE: "Sale toggle",
        INVOICE_REQUESTED: "Invoice requested",
        INVOICE_DELETED: "Invoice deleted",
        INVOICE_SENT: "Invoice sent",
        CUSTOMER_CREATED: "Customer created",
        CUSTOMER_UPDATED: "Customer updated",
        CUSTOMER_DELETED: "Customer deleted",
        COLLECTION_CREATED: "Collection created",
        COLLECTION_UPDATED: "Collection updated",
        COLLECTION_DELETED: "Collection deleted",
        PRODUCT_CREATED: "Product created",
        PRODUCT_UPDATED: "Product updated",
        PRODUCT_DELETED: "Product deleted",
        PRODUCT_VARIANT_CREATED: "Product variant created",
        PRODUCT_VARIANT_UPDATED: "Product variant updated",
        PRODUCT_VARIANT_DELETED: "Product variant deleted",
        PRODUCT_VARIANT_OUT_OF_STOCK: "Product variant stock changed",
        PRODUCT_VARIANT_BACK_IN_STOCK: "Product variant back in stock",
        CHECKOUT_CREATED: "Checkout created",
        CHECKOUT_UPDATED: "Checkout updated",
        FULFILLMENT_CREATED: "Fulfillment created",
        FULFILLMENT_CANCELED: "Fulfillment cancelled",
        FULFILLMENT_APPROVED: "Fulfillment approved",
        NOTIFY_USER: "Notify user",
        PAGE_CREATED: "Page Created",
        PAGE_UPDATED: "Page Updated",
        PAGE_DELETED: "Page Deleted",
        PAGE_TYPE_CREATED: "Page type created",
        PAGE_TYPE_UPDATED: "Page type updated",
        PAGE_TYPE_DELETED: "Page type deleted",
        PERMISSION_GROUP_CREATED: "Permission group created",
        PERMISSION_GROUP_UPDATED: "Permission group updated",
        PERMISSION_GROUP_DELETED: "Permission group deleted",
        SHIPPING_PRICE_CREATED: "Shipping price created",
        SHIPPING_PRICE_UPDATED: "Shipping price updated",
        SHIPPING_PRICE_DELETED: "Shipping price deleted",
        SHIPPING_ZONE_CREATED: "Shipping zone created",
        SHIPPING_ZONE_UPDATED: "Shipping zone updated",
        SHIPPING_ZONE_DELETED: "Shipping zone deleted",
        STAFF_CREATED: "Staff created",
        STAFF_UPDATED: "Staff updated",
        STAFF_DELETED: "Staff deleted",
        TRANSACTION_ACTION_REQUEST: "Payment action request",
        TRANSLATION_CREATED: "Create translation",
        TRANSLATION_UPDATED: "Update translation",
        WAREHOUSE_CREATED: "Warehouse created",
        WAREHOUSE_UPDATED: "Warehouse updated",
        WAREHOUSE_DELETED: "Warehouse deleted",
        VOUCHER_CREATED: "Voucher created",
        VOUCHER_UPDATED: "Voucher updated",
        VOUCHER_DELETED: "Voucher deleted",
        OBSERVABILITY: "Observability",
    }

    CHOICES = [
        (ANY, DISPLAY_LABELS[ANY]),
        (ADDRESS_CREATED, DISPLAY_LABELS[ADDRESS_CREATED]),
        (ADDRESS_UPDATED, DISPLAY_LABELS[ADDRESS_UPDATED]),
        (ADDRESS_DELETED, DISPLAY_LABELS[ADDRESS_DELETED]),
        (APP_INSTALLED, DISPLAY_LABELS[APP_INSTALLED]),
        (APP_UPDATED, DISPLAY_LABELS[APP_UPDATED]),
        (APP_DELETED, DISPLAY_LABELS[APP_DELETED]),
        (APP_STATUS_CHANGED, DISPLAY_LABELS[APP_STATUS_CHANGED]),
        (ATTRIBUTE_CREATED, DISPLAY_LABELS[ATTRIBUTE_CREATED]),
        (ATTRIBUTE_UPDATED, DISPLAY_LABELS[ATTRIBUTE_UPDATED]),
        (ATTRIBUTE_DELETED, DISPLAY_LABELS[ATTRIBUTE_DELETED]),
        (ATTRIBUTE_VALUE_CREATED, DISPLAY_LABELS[ATTRIBUTE_VALUE_CREATED]),
        (ATTRIBUTE_VALUE_UPDATED, DISPLAY_LABELS[ATTRIBUTE_VALUE_UPDATED]),
        (ATTRIBUTE_VALUE_DELETED, DISPLAY_LABELS[ATTRIBUTE_VALUE_DELETED]),
        (CATEGORY_CREATED, DISPLAY_LABELS[CATEGORY_CREATED]),
        (CATEGORY_UPDATED, DISPLAY_LABELS[CATEGORY_UPDATED]),
        (CATEGORY_DELETED, DISPLAY_LABELS[CATEGORY_DELETED]),
        (CHANNEL_CREATED, DISPLAY_LABELS[CHANNEL_CREATED]),
        (CHANNEL_UPDATED, DISPLAY_LABELS[CHANNEL_UPDATED]),
        (CHANNEL_DELETED, DISPLAY_LABELS[CHANNEL_DELETED]),
        (CHANNEL_STATUS_CHANGED, DISPLAY_LABELS[CHANNEL_STATUS_CHANGED]),
        (GIFT_CARD_CREATED, DISPLAY_LABELS[GIFT_CARD_CREATED]),
        (GIFT_CARD_UPDATED, DISPLAY_LABELS[GIFT_CARD_UPDATED]),
        (GIFT_CARD_DELETED, DISPLAY_LABELS[GIFT_CARD_DELETED]),
        (GIFT_CARD_STATUS_CHANGED, DISPLAY_LABELS[GIFT_CARD_STATUS_CHANGED]),
        (MENU_CREATED, DISPLAY_LABELS[MENU_CREATED]),
        (MENU_UPDATED, DISPLAY_LABELS[MENU_UPDATED]),
        (MENU_DELETED, DISPLAY_LABELS[MENU_DELETED]),
        (MENU_ITEM_CREATED, DISPLAY_LABELS[MENU_ITEM_CREATED]),
        (MENU_ITEM_UPDATED, DISPLAY_LABELS[MENU_ITEM_UPDATED]),
        (MENU_ITEM_DELETED, DISPLAY_LABELS[MENU_ITEM_DELETED]),
        (ORDER_CREATED, DISPLAY_LABELS[ORDER_CREATED]),
        (ORDER_CONFIRMED, DISPLAY_LABELS[ORDER_CONFIRMED]),
        (ORDER_FULLY_PAID, DISPLAY_LABELS[ORDER_FULLY_PAID]),
        (ORDER_UPDATED, DISPLAY_LABELS[ORDER_UPDATED]),
        (ORDER_CANCELLED, DISPLAY_LABELS[ORDER_CANCELLED]),
        (ORDER_FULFILLED, DISPLAY_LABELS[ORDER_FULFILLED]),
        (DRAFT_ORDER_CREATED, DISPLAY_LABELS[DRAFT_ORDER_CREATED]),
        (DRAFT_ORDER_UPDATED, DISPLAY_LABELS[DRAFT_ORDER_UPDATED]),
        (DRAFT_ORDER_DELETED, DISPLAY_LABELS[DRAFT_ORDER_DELETED]),
        (SALE_CREATED, DISPLAY_LABELS[SALE_CREATED]),
        (SALE_UPDATED, DISPLAY_LABELS[SALE_UPDATED]),
        (SALE_DELETED, DISPLAY_LABELS[SALE_DELETED]),
        (SALE_TOGGLE, DISPLAY_LABELS[SALE_TOGGLE]),
        (INVOICE_REQUESTED, DISPLAY_LABELS[INVOICE_REQUESTED]),
        (INVOICE_DELETED, DISPLAY_LABELS[INVOICE_DELETED]),
        (INVOICE_SENT, DISPLAY_LABELS[INVOICE_SENT]),
        (CUSTOMER_CREATED, DISPLAY_LABELS[CUSTOMER_CREATED]),
        (CUSTOMER_UPDATED, DISPLAY_LABELS[CUSTOMER_UPDATED]),
        (CUSTOMER_DELETED, DISPLAY_LABELS[CUSTOMER_DELETED]),
        (COLLECTION_CREATED, DISPLAY_LABELS[COLLECTION_CREATED]),
        (COLLECTION_UPDATED, DISPLAY_LABELS[COLLECTION_UPDATED]),
        (COLLECTION_DELETED, DISPLAY_LABELS[COLLECTION_DELETED]),
        (PRODUCT_CREATED, DISPLAY_LABELS[PRODUCT_CREATED]),
        (PRODUCT_UPDATED, DISPLAY_LABELS[PRODUCT_UPDATED]),
        (PRODUCT_DELETED, DISPLAY_LABELS[PRODUCT_DELETED]),
        (PRODUCT_VARIANT_CREATED, DISPLAY_LABELS[PRODUCT_VARIANT_CREATED]),
        (PRODUCT_VARIANT_UPDATED, DISPLAY_LABELS[PRODUCT_VARIANT_UPDATED]),
        (PRODUCT_VARIANT_DELETED, DISPLAY_LABELS[PRODUCT_VARIANT_DELETED]),
        (PRODUCT_VARIANT_OUT_OF_STOCK, DISPLAY_LABELS[PRODUCT_VARIANT_OUT_OF_STOCK]),
        (PRODUCT_VARIANT_BACK_IN_STOCK, DISPLAY_LABELS[PRODUCT_VARIANT_BACK_IN_STOCK]),
        (CHECKOUT_CREATED, DISPLAY_LABELS[CHECKOUT_CREATED]),
        (CHECKOUT_UPDATED, DISPLAY_LABELS[CHECKOUT_UPDATED]),
        (FULFILLMENT_CREATED, DISPLAY_LABELS[FULFILLMENT_CREATED]),
        (FULFILLMENT_CANCELED, DISPLAY_LABELS[FULFILLMENT_CANCELED]),
        (FULFILLMENT_APPROVED, DISPLAY_LABELS[FULFILLMENT_APPROVED]),
        (NOTIFY_USER, DISPLAY_LABELS[NOTIFY_USER]),
        (PAGE_CREATED, DISPLAY_LABELS[PAGE_CREATED]),
        (PAGE_UPDATED, DISPLAY_LABELS[PAGE_UPDATED]),
        (PAGE_DELETED, DISPLAY_LABELS[PAGE_DELETED]),
        (PAGE_TYPE_CREATED, DISPLAY_LABELS[PAGE_TYPE_CREATED]),
        (PAGE_TYPE_UPDATED, DISPLAY_LABELS[PAGE_TYPE_UPDATED]),
        (PAGE_TYPE_DELETED, DISPLAY_LABELS[PAGE_TYPE_DELETED]),
        (PERMISSION_GROUP_CREATED, DISPLAY_LABELS[PERMISSION_GROUP_CREATED]),
        (PERMISSION_GROUP_UPDATED, DISPLAY_LABELS[PERMISSION_GROUP_UPDATED]),
        (PERMISSION_GROUP_DELETED, DISPLAY_LABELS[PERMISSION_GROUP_DELETED]),
        (SHIPPING_PRICE_CREATED, DISPLAY_LABELS[SHIPPING_PRICE_CREATED]),
        (SHIPPING_PRICE_UPDATED, DISPLAY_LABELS[SHIPPING_PRICE_UPDATED]),
        (SHIPPING_PRICE_DELETED, DISPLAY_LABELS[SHIPPING_PRICE_DELETED]),
        (SHIPPING_ZONE_CREATED, DISPLAY_LABELS[SHIPPING_ZONE_CREATED]),
        (SHIPPING_ZONE_UPDATED, DISPLAY_LABELS[SHIPPING_ZONE_UPDATED]),
        (SHIPPING_ZONE_DELETED, DISPLAY_LABELS[SHIPPING_ZONE_DELETED]),
        (STAFF_CREATED, DISPLAY_LABELS[STAFF_CREATED]),
        (STAFF_UPDATED, DISPLAY_LABELS[STAFF_UPDATED]),
        (STAFF_DELETED, DISPLAY_LABELS[STAFF_DELETED]),
        (TRANSACTION_ACTION_REQUEST, DISPLAY_LABELS[TRANSACTION_ACTION_REQUEST]),
        (TRANSLATION_CREATED, DISPLAY_LABELS[TRANSLATION_CREATED]),
        (TRANSLATION_UPDATED, DISPLAY_LABELS[TRANSLATION_UPDATED]),
        (WAREHOUSE_CREATED, DISPLAY_LABELS[WAREHOUSE_CREATED]),
        (WAREHOUSE_UPDATED, DISPLAY_LABELS[WAREHOUSE_UPDATED]),
        (WAREHOUSE_DELETED, DISPLAY_LABELS[WAREHOUSE_DELETED]),
        (VOUCHER_CREATED, DISPLAY_LABELS[VOUCHER_CREATED]),
        (VOUCHER_UPDATED, DISPLAY_LABELS[VOUCHER_UPDATED]),
        (VOUCHER_DELETED, DISPLAY_LABELS[VOUCHER_DELETED]),
        (OBSERVABILITY, DISPLAY_LABELS[OBSERVABILITY]),
=======
    THUMBNAIL_CREATED = "thumbnail_created"

    SHOP_METADATA_UPDATED = "shop_metadata_updated"

    EVENT_MAP: dict[str, dict[str, Any]] = {
        ACCOUNT_CONFIRMATION_REQUESTED: {
            "name": "Account confirmation requested",
            "permission": AccountPermissions.MANAGE_USERS,
        },
        ACCOUNT_CHANGE_EMAIL_REQUESTED: {
            "name": "Account change email requested",
            "permission": AccountPermissions.MANAGE_USERS,
        },
        ACCOUNT_EMAIL_CHANGED: {
            "name": "Account email changed",
            "permission": AccountPermissions.MANAGE_USERS,
        },
        ACCOUNT_SET_PASSWORD_REQUESTED: {
            "name": "Account set password requested",
            "permission": AccountPermissions.MANAGE_USERS,
        },
        ACCOUNT_CONFIRMED: {
            "name": "Account confirmed",
            "permission": AccountPermissions.MANAGE_USERS,
        },
        ACCOUNT_DELETE_REQUESTED: {
            "name": "Account delete requested",
            "permission": AccountPermissions.MANAGE_USERS,
        },
        ACCOUNT_DELETED: {
            "name": "Account delete confirmed",
            "permission": AccountPermissions.MANAGE_USERS,
        },
        ADDRESS_CREATED: {
            "name": "Address created",
            "permission": AccountPermissions.MANAGE_USERS,
        },
        ADDRESS_UPDATED: {
            "name": "Address updated",
            "permission": AccountPermissions.MANAGE_USERS,
        },
        ADDRESS_DELETED: {
            "name": "Address deleted",
            "permission": AccountPermissions.MANAGE_USERS,
        },
        APP_INSTALLED: {
            "name": "App created",
            "permission": AppPermission.MANAGE_APPS,
        },
        APP_UPDATED: {
            "name": "App updated",
            "permission": AppPermission.MANAGE_APPS,
        },
        APP_DELETED: {
            "name": "App deleted",
            "permission": AppPermission.MANAGE_APPS,
        },
        APP_STATUS_CHANGED: {
            "name": "App status changed",
            "permission": AppPermission.MANAGE_APPS,
        },
        ATTRIBUTE_CREATED: {
            "name": "Attribute created",
            "permission": None,
        },
        ATTRIBUTE_UPDATED: {
            "name": "Attribute updated",
            "permission": None,
        },
        ATTRIBUTE_DELETED: {
            "name": "Attribute deleted",
            "permission": None,
        },
        ATTRIBUTE_VALUE_CREATED: {
            "name": "Attribute value created",
            "permission": None,
        },
        ATTRIBUTE_VALUE_UPDATED: {
            "name": "Attribute value updated",
            "permission": None,
        },
        ATTRIBUTE_VALUE_DELETED: {
            "name": "Attribute value deleted",
            "permission": None,
        },
        CATEGORY_CREATED: {
            "name": "Category created",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        CATEGORY_UPDATED: {
            "name": "Category updated",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        CATEGORY_DELETED: {
            "name": "Category deleted",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        CHANNEL_CREATED: {
            "name": "Channel created",
            "permission": ChannelPermissions.MANAGE_CHANNELS,
        },
        CHANNEL_UPDATED: {
            "name": "Channel updated",
            "permission": ChannelPermissions.MANAGE_CHANNELS,
        },
        CHANNEL_DELETED: {
            "name": "Channel deleted",
            "permission": ChannelPermissions.MANAGE_CHANNELS,
        },
        CHANNEL_STATUS_CHANGED: {
            "name": "Channel status changed",
            "permission": ChannelPermissions.MANAGE_CHANNELS,
        },
        CHANNEL_METADATA_UPDATED: {
            "name": "Channel metadata updated",
            "permission": ChannelPermissions.MANAGE_CHANNELS,
        },
        GIFT_CARD_CREATED: {
            "name": "Gift card created",
            "permission": GiftcardPermissions.MANAGE_GIFT_CARD,
        },
        GIFT_CARD_UPDATED: {
            "name": "Gift card updated",
            "permission": GiftcardPermissions.MANAGE_GIFT_CARD,
        },
        GIFT_CARD_DELETED: {
            "name": "Gift card deleted",
            "permission": GiftcardPermissions.MANAGE_GIFT_CARD,
        },
        GIFT_CARD_SENT: {
            "name": "Gift card sent",
            "permission": GiftcardPermissions.MANAGE_GIFT_CARD,
        },
        GIFT_CARD_STATUS_CHANGED: {
            "name": "Gift card status changed",
            "permission": GiftcardPermissions.MANAGE_GIFT_CARD,
        },
        GIFT_CARD_METADATA_UPDATED: {
            "name": "Gift card metadata updated",
            "permission": GiftcardPermissions.MANAGE_GIFT_CARD,
        },
        GIFT_CARD_EXPORT_COMPLETED: {
            "name": "Gift card export completed",
            "permission": GiftcardPermissions.MANAGE_GIFT_CARD,
        },
        MENU_CREATED: {
            "name": "Menu created",
            "permission": MenuPermissions.MANAGE_MENUS,
        },
        MENU_UPDATED: {
            "name": "Menu updated",
            "permission": MenuPermissions.MANAGE_MENUS,
        },
        MENU_DELETED: {
            "name": "Menu deleted",
            "permission": MenuPermissions.MANAGE_MENUS,
        },
        MENU_ITEM_CREATED: {
            "name": "Menu item created",
            "permission": MenuPermissions.MANAGE_MENUS,
        },
        MENU_ITEM_UPDATED: {
            "name": "Menu item updated",
            "permission": MenuPermissions.MANAGE_MENUS,
        },
        MENU_ITEM_DELETED: {
            "name": "Menu item deleted",
            "permission": MenuPermissions.MANAGE_MENUS,
        },
        ORDER_CREATED: {
            "name": "Order created",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        ORDER_CONFIRMED: {
            "name": "Order confirmed",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        ORDER_PAID: {
            "name": "Order paid",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        ORDER_FULLY_PAID: {
            "name": "Order fully paid",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        ORDER_REFUNDED: {
            "name": "Order refunded",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        ORDER_FULLY_REFUNDED: {
            "name": "Order fully refunded",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        ORDER_UPDATED: {
            "name": "Order updated",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        ORDER_CANCELLED: {
            "name": "Order cancelled",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        ORDER_EXPIRED: {
            "name": "Order expired",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        ORDER_FULFILLED: {
            "name": "Order fulfilled",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        ORDER_METADATA_UPDATED: {
            "name": "Order metadata updated",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        ORDER_BULK_CREATED: {
            "name": "Order bulk created",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        FULFILLMENT_CREATED: {
            "name": "Fulfillment created",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        FULFILLMENT_CANCELED: {
            "name": "Fulfillment cancelled",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        FULFILLMENT_APPROVED: {
            "name": "Fulfillment approved",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        FULFILLMENT_METADATA_UPDATED: {
            "name": "Fulfillment metadata updated",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        FULFILLMENT_TRACKING_NUMBER_UPDATED: {
            "name": "Fulfillment tracking number updated.",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        DRAFT_ORDER_CREATED: {
            "name": "Draft order created",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        DRAFT_ORDER_UPDATED: {
            "name": "Draft order updated",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        DRAFT_ORDER_DELETED: {
            "name": "Draft order deleted",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        SALE_CREATED: {
            "name": "Sale created",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        SALE_UPDATED: {
            "name": "Sale updated",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        SALE_DELETED: {
            "name": "Sale deleted",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        SALE_TOGGLE: {
            "name": "Sale toggle",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        PROMOTION_CREATED: {
            "name": "Promotion created",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        PROMOTION_UPDATED: {
            "name": "Promotion updated",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        PROMOTION_DELETED: {
            "name": "Promotion deleted",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        PROMOTION_STARTED: {
            "name": "Promotion started",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        PROMOTION_ENDED: {
            "name": "Promotion ended",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        PROMOTION_RULE_CREATED: {
            "name": "Promotion rule created",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        PROMOTION_RULE_UPDATED: {
            "name": "Promotion rule updated",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        PROMOTION_RULE_DELETED: {
            "name": "Promotion rule deleted",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        INVOICE_REQUESTED: {
            "name": "Invoice requested",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        INVOICE_DELETED: {
            "name": "Invoice deleted",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        INVOICE_SENT: {
            "name": "Invoice sent",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        CUSTOMER_CREATED: {
            "name": "Customer created",
            "permission": AccountPermissions.MANAGE_USERS,
        },
        CUSTOMER_UPDATED: {
            "name": "Customer updated",
            "permission": AccountPermissions.MANAGE_USERS,
        },
        CUSTOMER_DELETED: {
            "name": "Customer deleted",
            "permission": AccountPermissions.MANAGE_USERS,
        },
        CUSTOMER_METADATA_UPDATED: {
            "name": "Customer metadata updated",
            "permission": AccountPermissions.MANAGE_USERS,
        },
        COLLECTION_CREATED: {
            "name": "Collection created",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        COLLECTION_UPDATED: {
            "name": "Collection updated",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        COLLECTION_DELETED: {
            "name": "Collection deleted",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        COLLECTION_METADATA_UPDATED: {
            "name": "Collection metadata updated",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        PRODUCT_CREATED: {
            "name": "Product created",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        PRODUCT_UPDATED: {
            "name": "Product updated",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        PRODUCT_DELETED: {
            "name": "Product deleted",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        PRODUCT_METADATA_UPDATED: {
            "name": "Product metadata updated",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        PRODUCT_EXPORT_COMPLETED: {
            "name": "Product export completed",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        PRODUCT_MEDIA_CREATED: {
            "name": "Product media created",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        PRODUCT_MEDIA_UPDATED: {
            "name": "Product media updated",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        PRODUCT_MEDIA_DELETED: {
            "name": "Product media deleted",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        PRODUCT_VARIANT_CREATED: {
            "name": "Product variant created",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        PRODUCT_VARIANT_UPDATED: {
            "name": "Product variant updated",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        PRODUCT_VARIANT_DELETED: {
            "name": "Product variant deleted",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        PRODUCT_VARIANT_METADATA_UPDATED: {
            "name": "Product variant metadata updated",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        PRODUCT_VARIANT_OUT_OF_STOCK: {
            "name": "Product variant stock changed",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        PRODUCT_VARIANT_BACK_IN_STOCK: {
            "name": "Product variant back in stock",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        PRODUCT_VARIANT_STOCK_UPDATED: {
            "name": "Product variant stock updated",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        CHECKOUT_CREATED: {
            "name": "Checkout created",
            "permission": CheckoutPermissions.MANAGE_CHECKOUTS,
        },
        CHECKOUT_UPDATED: {
            "name": "Checkout updated",
            "permission": CheckoutPermissions.MANAGE_CHECKOUTS,
        },
        CHECKOUT_FULLY_PAID: {
            "name": "Checkout fully paid",
            "permission": CheckoutPermissions.MANAGE_CHECKOUTS,
        },
        CHECKOUT_METADATA_UPDATED: {
            "name": "Checkout metadata updated",
            "permission": CheckoutPermissions.MANAGE_CHECKOUTS,
        },
        NOTIFY_USER: {
            "name": "Notify user",
            "permission": AccountPermissions.MANAGE_USERS,
        },
        PAGE_CREATED: {
            "name": "Page created",
            "permission": PagePermissions.MANAGE_PAGES,
        },
        PAGE_UPDATED: {
            "name": "Page updated",
            "permission": PagePermissions.MANAGE_PAGES,
        },
        PAGE_DELETED: {
            "name": "Page deleted",
            "permission": PagePermissions.MANAGE_PAGES,
        },
        PAGE_TYPE_CREATED: {
            "name": "Page type created",
            "permission": PageTypePermissions.MANAGE_PAGE_TYPES_AND_ATTRIBUTES,
        },
        PAGE_TYPE_UPDATED: {
            "name": "Page type updated",
            "permission": PageTypePermissions.MANAGE_PAGE_TYPES_AND_ATTRIBUTES,
        },
        PAGE_TYPE_DELETED: {
            "name": "Page type deleted",
            "permission": PageTypePermissions.MANAGE_PAGE_TYPES_AND_ATTRIBUTES,
        },
        PERMISSION_GROUP_CREATED: {
            "name": "Permission group created",
            "permission": AccountPermissions.MANAGE_STAFF,
        },
        PERMISSION_GROUP_UPDATED: {
            "name": "Permission group updated",
            "permission": AccountPermissions.MANAGE_STAFF,
        },
        PERMISSION_GROUP_DELETED: {
            "name": "Permission group deleted",
            "permission": AccountPermissions.MANAGE_STAFF,
        },
        SHIPPING_PRICE_CREATED: {
            "name": "Shipping price created",
            "permission": ShippingPermissions.MANAGE_SHIPPING,
        },
        SHIPPING_PRICE_UPDATED: {
            "name": "Shipping price updated",
            "permission": ShippingPermissions.MANAGE_SHIPPING,
        },
        SHIPPING_PRICE_DELETED: {
            "name": "Shipping price deleted",
            "permission": ShippingPermissions.MANAGE_SHIPPING,
        },
        SHIPPING_ZONE_CREATED: {
            "name": "Shipping zone created",
            "permission": ShippingPermissions.MANAGE_SHIPPING,
        },
        SHIPPING_ZONE_UPDATED: {
            "name": "Shipping zone updated",
            "permission": ShippingPermissions.MANAGE_SHIPPING,
        },
        SHIPPING_ZONE_DELETED: {
            "name": "Shipping zone deleted",
            "permission": ShippingPermissions.MANAGE_SHIPPING,
        },
        SHIPPING_ZONE_METADATA_UPDATED: {
            "name": "Shipping zone metadata updated",
            "permission": ShippingPermissions.MANAGE_SHIPPING,
        },
        STAFF_CREATED: {
            "name": "Staff created",
            "permission": AccountPermissions.MANAGE_STAFF,
        },
        STAFF_UPDATED: {
            "name": "Staff updated",
            "permission": AccountPermissions.MANAGE_STAFF,
        },
        STAFF_DELETED: {
            "name": "Staff deleted",
            "permission": AccountPermissions.MANAGE_STAFF,
        },
        STAFF_SET_PASSWORD_REQUESTED: {
            "name": "Setting a password for a staff is requested",
            "permission": AccountPermissions.MANAGE_STAFF,
        },
        TRANSACTION_ITEM_METADATA_UPDATED: {
            "name": "Transaction item metadata updated",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
        TRANSLATION_CREATED: {
            "name": "Translation created",
            "permission": SitePermissions.MANAGE_TRANSLATIONS,
        },
        TRANSLATION_UPDATED: {
            "name": "Translation updated",
            "permission": SitePermissions.MANAGE_TRANSLATIONS,
        },
        WAREHOUSE_CREATED: {
            "name": "Warehouse created",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        WAREHOUSE_UPDATED: {
            "name": "Warehouse updated",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        WAREHOUSE_DELETED: {
            "name": "Warehouse deleted",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        WAREHOUSE_METADATA_UPDATED: {
            "name": "Warehouse metadata updated",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        VOUCHER_CREATED: {
            "name": "Voucher created",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        VOUCHER_UPDATED: {
            "name": "Voucher updated",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        VOUCHER_DELETED: {
            "name": "Voucher deleted",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        VOUCHER_CODES_CREATED: {
            "name": "Voucher codes created",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        VOUCHER_CODES_DELETED: {
            "name": "Voucher codes deleted",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        VOUCHER_METADATA_UPDATED: {
            "name": "Voucher metadata updated",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        VOUCHER_CODE_EXPORT_COMPLETED: {
            "name": "Voucher code export completed",
            "permission": DiscountPermissions.MANAGE_DISCOUNTS,
        },
        OBSERVABILITY: {
            "name": "Observability",
            "permission": AppPermission.MANAGE_OBSERVABILITY,
        },
        THUMBNAIL_CREATED: {
            "name": "Thumbnail created",
            "permission": ProductPermissions.MANAGE_PRODUCTS,
        },
        SHOP_METADATA_UPDATED: {
            "name": "Shop metadata updated",
            "permission": SitePermissions.MANAGE_SETTINGS,
        },
    }

    CHOICES = [
        (ANY, "Any events"),
    ] + [
        (event_name, event_data["name"]) for event_name, event_data in EVENT_MAP.items()
>>>>>>> fa9ea3af1251eaa792bebc0aabcf03f49b31a7e9
    ]
    PERMISSIONS: dict[str, Optional[BasePermissionEnum]] = {
        event_name: event_data["permission"]
        for event_name, event_data in EVENT_MAP.items()
    }

    ALL = [event[0] for event in CHOICES]

<<<<<<< HEAD
    PERMISSIONS = {
        ADDRESS_CREATED: AccountPermissions.MANAGE_USERS,
        ADDRESS_UPDATED: AccountPermissions.MANAGE_USERS,
        ADDRESS_DELETED: AccountPermissions.MANAGE_USERS,
        APP_INSTALLED: AppPermission.MANAGE_APPS,
        APP_UPDATED: AppPermission.MANAGE_APPS,
        APP_DELETED: AppPermission.MANAGE_APPS,
        APP_STATUS_CHANGED: AppPermission.MANAGE_APPS,
        ATTRIBUTE_CREATED: None,
        ATTRIBUTE_UPDATED: None,
        ATTRIBUTE_DELETED: None,
        ATTRIBUTE_VALUE_CREATED: None,
        ATTRIBUTE_VALUE_UPDATED: None,
        ATTRIBUTE_VALUE_DELETED: None,
        CATEGORY_CREATED: ProductPermissions.MANAGE_PRODUCTS,
        CATEGORY_UPDATED: ProductPermissions.MANAGE_PRODUCTS,
        CATEGORY_DELETED: ProductPermissions.MANAGE_PRODUCTS,
        CHANNEL_CREATED: ChannelPermissions.MANAGE_CHANNELS,
        CHANNEL_UPDATED: ChannelPermissions.MANAGE_CHANNELS,
        CHANNEL_DELETED: ChannelPermissions.MANAGE_CHANNELS,
        CHANNEL_STATUS_CHANGED: ChannelPermissions.MANAGE_CHANNELS,
        GIFT_CARD_CREATED: GiftcardPermissions.MANAGE_GIFT_CARD,
        GIFT_CARD_UPDATED: GiftcardPermissions.MANAGE_GIFT_CARD,
        GIFT_CARD_DELETED: GiftcardPermissions.MANAGE_GIFT_CARD,
        GIFT_CARD_STATUS_CHANGED: GiftcardPermissions.MANAGE_GIFT_CARD,
        MENU_CREATED: MenuPermissions.MANAGE_MENUS,
        MENU_UPDATED: MenuPermissions.MANAGE_MENUS,
        MENU_DELETED: MenuPermissions.MANAGE_MENUS,
        MENU_ITEM_CREATED: MenuPermissions.MANAGE_MENUS,
        MENU_ITEM_UPDATED: MenuPermissions.MANAGE_MENUS,
        MENU_ITEM_DELETED: MenuPermissions.MANAGE_MENUS,
        ORDER_CREATED: OrderPermissions.MANAGE_ORDERS,
        ORDER_CONFIRMED: OrderPermissions.MANAGE_ORDERS,
        ORDER_FULLY_PAID: OrderPermissions.MANAGE_ORDERS,
        ORDER_UPDATED: OrderPermissions.MANAGE_ORDERS,
        ORDER_CANCELLED: OrderPermissions.MANAGE_ORDERS,
        ORDER_FULFILLED: OrderPermissions.MANAGE_ORDERS,
        DRAFT_ORDER_CREATED: OrderPermissions.MANAGE_ORDERS,
        DRAFT_ORDER_DELETED: OrderPermissions.MANAGE_ORDERS,
        DRAFT_ORDER_UPDATED: OrderPermissions.MANAGE_ORDERS,
        SALE_CREATED: DiscountPermissions.MANAGE_DISCOUNTS,
        SALE_UPDATED: DiscountPermissions.MANAGE_DISCOUNTS,
        SALE_DELETED: DiscountPermissions.MANAGE_DISCOUNTS,
        SALE_TOGGLE: DiscountPermissions.MANAGE_DISCOUNTS,
        INVOICE_REQUESTED: OrderPermissions.MANAGE_ORDERS,
        INVOICE_DELETED: OrderPermissions.MANAGE_ORDERS,
        INVOICE_SENT: OrderPermissions.MANAGE_ORDERS,
        CUSTOMER_CREATED: AccountPermissions.MANAGE_USERS,
        CUSTOMER_UPDATED: AccountPermissions.MANAGE_USERS,
        CUSTOMER_DELETED: AccountPermissions.MANAGE_USERS,
        COLLECTION_CREATED: ProductPermissions.MANAGE_PRODUCTS,
        COLLECTION_UPDATED: ProductPermissions.MANAGE_PRODUCTS,
        COLLECTION_DELETED: ProductPermissions.MANAGE_PRODUCTS,
        PRODUCT_CREATED: ProductPermissions.MANAGE_PRODUCTS,
        PRODUCT_UPDATED: ProductPermissions.MANAGE_PRODUCTS,
        PRODUCT_DELETED: ProductPermissions.MANAGE_PRODUCTS,
        PRODUCT_VARIANT_CREATED: ProductPermissions.MANAGE_PRODUCTS,
        PRODUCT_VARIANT_UPDATED: ProductPermissions.MANAGE_PRODUCTS,
        PRODUCT_VARIANT_DELETED: ProductPermissions.MANAGE_PRODUCTS,
        PRODUCT_VARIANT_BACK_IN_STOCK: ProductPermissions.MANAGE_PRODUCTS,
        PRODUCT_VARIANT_OUT_OF_STOCK: ProductPermissions.MANAGE_PRODUCTS,
        CHECKOUT_CREATED: CheckoutPermissions.MANAGE_CHECKOUTS,
        CHECKOUT_UPDATED: CheckoutPermissions.MANAGE_CHECKOUTS,
        FULFILLMENT_CREATED: OrderPermissions.MANAGE_ORDERS,
        FULFILLMENT_CANCELED: OrderPermissions.MANAGE_ORDERS,
        FULFILLMENT_APPROVED: OrderPermissions.MANAGE_ORDERS,
        NOTIFY_USER: AccountPermissions.MANAGE_USERS,
        PAGE_CREATED: PagePermissions.MANAGE_PAGES,
        PAGE_UPDATED: PagePermissions.MANAGE_PAGES,
        PAGE_DELETED: PagePermissions.MANAGE_PAGES,
        PAGE_TYPE_CREATED: PageTypePermissions.MANAGE_PAGE_TYPES_AND_ATTRIBUTES,
        PAGE_TYPE_UPDATED: PageTypePermissions.MANAGE_PAGE_TYPES_AND_ATTRIBUTES,
        PAGE_TYPE_DELETED: PageTypePermissions.MANAGE_PAGE_TYPES_AND_ATTRIBUTES,
        PERMISSION_GROUP_CREATED: AccountPermissions.MANAGE_STAFF,
        PERMISSION_GROUP_UPDATED: AccountPermissions.MANAGE_STAFF,
        PERMISSION_GROUP_DELETED: AccountPermissions.MANAGE_STAFF,
        SHIPPING_PRICE_CREATED: ShippingPermissions.MANAGE_SHIPPING,
        SHIPPING_PRICE_UPDATED: ShippingPermissions.MANAGE_SHIPPING,
        SHIPPING_PRICE_DELETED: ShippingPermissions.MANAGE_SHIPPING,
        SHIPPING_ZONE_CREATED: ShippingPermissions.MANAGE_SHIPPING,
        SHIPPING_ZONE_UPDATED: ShippingPermissions.MANAGE_SHIPPING,
        SHIPPING_ZONE_DELETED: ShippingPermissions.MANAGE_SHIPPING,
        STAFF_CREATED: AccountPermissions.MANAGE_STAFF,
        STAFF_UPDATED: AccountPermissions.MANAGE_STAFF,
        STAFF_DELETED: AccountPermissions.MANAGE_STAFF,
        TRANSACTION_ACTION_REQUEST: PaymentPermissions.HANDLE_PAYMENTS,
        TRANSLATION_CREATED: SitePermissions.MANAGE_TRANSLATIONS,
        TRANSLATION_UPDATED: SitePermissions.MANAGE_TRANSLATIONS,
        VOUCHER_CREATED: DiscountPermissions.MANAGE_DISCOUNTS,
        VOUCHER_UPDATED: DiscountPermissions.MANAGE_DISCOUNTS,
        VOUCHER_DELETED: DiscountPermissions.MANAGE_DISCOUNTS,
        WAREHOUSE_CREATED: ProductPermissions.MANAGE_PRODUCTS,
        WAREHOUSE_UPDATED: ProductPermissions.MANAGE_PRODUCTS,
        WAREHOUSE_DELETED: ProductPermissions.MANAGE_PRODUCTS,
        OBSERVABILITY: AppPermission.MANAGE_OBSERVABILITY,
    }

=======
>>>>>>> fa9ea3af1251eaa792bebc0aabcf03f49b31a7e9

class WebhookEventSyncType:
    PAYMENT_LIST_GATEWAYS = "payment_list_gateways"
    PAYMENT_AUTHORIZE = "payment_authorize"
    PAYMENT_CAPTURE = "payment_capture"
    PAYMENT_REFUND = "payment_refund"
    PAYMENT_VOID = "payment_void"
    PAYMENT_CONFIRM = "payment_confirm"
    PAYMENT_PROCESS = "payment_process"

    CHECKOUT_CALCULATE_TAXES = "checkout_calculate_taxes"
    ORDER_CALCULATE_TAXES = "order_calculate_taxes"

    TRANSACTION_CHARGE_REQUESTED = "transaction_charge_requested"
    TRANSACTION_REFUND_REQUESTED = "transaction_refund_requested"
    TRANSACTION_CANCELATION_REQUESTED = "transaction_cancelation_requested"

    SHIPPING_LIST_METHODS_FOR_CHECKOUT = "shipping_list_methods_for_checkout"
    CHECKOUT_FILTER_SHIPPING_METHODS = "checkout_filter_shipping_methods"
    ORDER_FILTER_SHIPPING_METHODS = "order_filter_shipping_methods"

    PAYMENT_GATEWAY_INITIALIZE_SESSION = "payment_gateway_initialize_session"
    TRANSACTION_INITIALIZE_SESSION = "transaction_initialize_session"
    TRANSACTION_PROCESS_SESSION = "transaction_process_session"

    LIST_STORED_PAYMENT_METHODS = "list_stored_payment_methods"
    STORED_PAYMENT_METHOD_DELETE_REQUESTED = "stored_payment_method_delete_requested"

    PAYMENT_GATEWAY_INITIALIZE_TOKENIZATION_SESSION = (
        "payment_gateway_initialize_tokenization_session"
    )
    PAYMENT_METHOD_INITIALIZE_TOKENIZATION_SESSION = (
        "payment_method_initialize_tokenization_session"
    )
    PAYMENT_METHOD_PROCESS_TOKENIZATION_SESSION = (
        "payment_method_process_tokenization_session"
    )

    EVENT_MAP: dict[str, dict[str, Any]] = {
        PAYMENT_LIST_GATEWAYS: {
            "name": "List payment gateways",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
        PAYMENT_AUTHORIZE: {
            "name": "Authorize payment",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
        PAYMENT_CAPTURE: {
            "name": "Capture payment",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
        PAYMENT_REFUND: {
            "name": "Refund payment",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
        PAYMENT_VOID: {
            "name": "Void payment",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
        PAYMENT_CONFIRM: {
            "name": "Confirm payment",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
        PAYMENT_PROCESS: {
            "name": "Process payment",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
        CHECKOUT_CALCULATE_TAXES: {
            "name": "Calculate taxes for checkout",
            "permission": CheckoutPermissions.HANDLE_TAXES,
        },
        ORDER_CALCULATE_TAXES: {
            "name": "Calculate taxes for order",
            "permission": CheckoutPermissions.HANDLE_TAXES,
        },
        TRANSACTION_CHARGE_REQUESTED: {
            "name": "Transaction charge requested",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
        TRANSACTION_REFUND_REQUESTED: {
            "name": "Transaction refund requested",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
        TRANSACTION_CANCELATION_REQUESTED: {
            "name": "Transaction cancelation requested",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
        SHIPPING_LIST_METHODS_FOR_CHECKOUT: {
            "name": "List shipping methods for checkout",
            "permission": ShippingPermissions.MANAGE_SHIPPING,
        },
        CHECKOUT_FILTER_SHIPPING_METHODS: {
            "name": "Filter shipping methods for checkout",
            "permission": CheckoutPermissions.MANAGE_CHECKOUTS,
        },
        ORDER_FILTER_SHIPPING_METHODS: {
            "name": "Filter shipping methods for order",
            "permission": OrderPermissions.MANAGE_ORDERS,
        },
        PAYMENT_GATEWAY_INITIALIZE_SESSION: {
            "name": "Initialize payment gateway session",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
        TRANSACTION_INITIALIZE_SESSION: {
            "name": "Initialize transaction session",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
        TRANSACTION_PROCESS_SESSION: {
            "name": "Process transaction session",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
        LIST_STORED_PAYMENT_METHODS: {
            "name": "List tokenized payment methods that can be used by the customer.",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
        STORED_PAYMENT_METHOD_DELETE_REQUESTED: {
            "name": "Request deletion of a tokenized payment method.",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
        PAYMENT_GATEWAY_INITIALIZE_TOKENIZATION_SESSION: {
            "name": "Initialize payment gateway tokenization session.",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
        PAYMENT_METHOD_INITIALIZE_TOKENIZATION_SESSION: {
            "name": "Initialize payment method tokenization session.",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
        PAYMENT_METHOD_PROCESS_TOKENIZATION_SESSION: {
            "name": "Process payment method tokenization.",
            "permission": PaymentPermissions.HANDLE_PAYMENTS,
        },
    }

    CHOICES = [
        (event_name, event_data["name"]) for event_name, event_data in EVENT_MAP.items()
    ]
    PERMISSIONS: dict[str, Optional[BasePermissionEnum]] = {
        event_name: event_data["permission"]
        for event_name, event_data in EVENT_MAP.items()
    }

    ALL = [event[0] for event in CHOICES]

    PAYMENT_EVENTS = [
        PAYMENT_AUTHORIZE,
        PAYMENT_CAPTURE,
        PAYMENT_CONFIRM,
        PAYMENT_LIST_GATEWAYS,
        PAYMENT_PROCESS,
        PAYMENT_REFUND,
        PAYMENT_VOID,
    ]

    # Events that are used only in the mutation logic can be excluded from the
    # circular query check.
    ALLOWED_IN_CIRCULAR_QUERY = [
        PAYMENT_GATEWAY_INITIALIZE_SESSION,
        TRANSACTION_INITIALIZE_SESSION,
        TRANSACTION_PROCESS_SESSION,
        TRANSACTION_CHARGE_REQUESTED,
        TRANSACTION_REFUND_REQUESTED,
        TRANSACTION_CANCELATION_REQUESTED,
    ]
