import stripe
from config.settings import STRIPE_API_KEY


stripe.api_key = STRIPE_API_KEY

def create_stripe_product(name):
    """
    Создание продукта в Stripe
    """
    product = stripe.Product.create(
        name=name
    )
    return product.name


def create_stripe_price(amount, name):
    """
    Создание цены на продукт в Stripe
    """
    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": name},
    )
    return price


def create_stripe_session(price):
    """
    Создание сессии платежа Stripe
    """
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000",
        line_items=[
            {"price": price, "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url"), session.get("payment_status")


def get_stripe_payment_status(session_id):
    """
    Получение статуса платежа от Stripe
    """
    session = stripe.checkout.Session.retrieve(session_id,)
    print(session.get("payment_status"))
    return session.get("payment_status")