from .models import Customer


def customers_from_id(customer_ids):
    customer_objs = Customer.objects.filter(customer_id__in=customer_ids)
    customers = []
    for obj in customer_objs:
        customers.append({"customer_id": obj.customer_id, "customer_name": obj.customer_name})
    return customers
