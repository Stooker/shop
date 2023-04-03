from .models import Cart, ProductCart


def add_to_cart(product, quantity, cart):
    product.quantity -= quantity # zmniejszenie ilosci na stanie
    product.save(update_fields=['quantity'])

    product_cart, _ = ProductCart.objects.get_or_create(cart=cart, product=product)
    product_cart.quantity += quantity # zwiekszenie ilosci w koszyku
    product_cart.save(update_fields=['quantity'])

    return
