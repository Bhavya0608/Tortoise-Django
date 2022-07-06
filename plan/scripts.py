from datetime import date

from .models import CustomerGoal, Plan, PlanOption, Promotion
from django.db.models import F


def plan_from_id(plan_id, plan_object_id=None):
    plan_obj = Plan.objects.get(plan_id=plan_id)
    plan_option_objs = PlanOption.objects.filter(plan_id=plan_id)
    plan = []
    for obj in plan_option_objs:
        if plan_object_id is None or (plan_object_id is not None and int(plan_object_id) == obj.plan_option_id):
            plan.append({"plan_id": plan_obj.plan_id, "plan_name": plan_obj.plan_name, "benefit_per": plan_obj.benefit_per,
            "benefit_type": plan_obj.benefit_type, "plan_option_id": obj.plan_option_id, "amount_option": obj.amount_option,
            "tenure_option": obj.tenure_option})
    return plan


def get_all_plans():
    plan_ids = Plan.objects.filter(is_active=True).values_list('plan_id', flat=True)
    plans = []
    for plan_id in plan_ids:
        plans.extend(plan_from_id(plan_id=plan_id))
    return plans


def promotions_from_id(plan_id):
    today = date.today()
    print(today)
    promo_values = Promotion.objects.filter(plan_id=Plan.objects.get(plan_id=plan_id)).filter(curr_user__lt=F('max_user')).filter(end_date__gte=today).values("promo_id", 
    "curr_user", "max_user", "start_date", "end_date", "promo_per")
    promotions = list(promo_values)
    return promotions


def use_promotion(promo_id):
    po = Promotion.objects.get(promo_id=promo_id)
    po.curr_user = po.curr_user + 1
    po.save()
    return po.curr_user


def deposit_amount(customer_goal_id):
    cg = CustomerGoal.objects.get(customer_goal_id=customer_goal_id)
    cg.deposited_amount = cg.deposited_amount + cg.plan_option_id.amount_option
    cg.save()


def get_customer_goal_from_id(customer_goal_id):
    customer_goal_obj = CustomerGoal.objects.get(customer_goal_id=customer_goal_id)
    plan = plan_from_id(plan_id=customer_goal_obj.plan_id.plan_id, plan_object_id=customer_goal_obj.plan_option_id.plan_option_id)[0]
    customer_goal = {"customer_goal_id": customer_goal_obj.customer_goal_id,
                    "deposited_amount": customer_goal_obj.deposited_amount,
                    "total_amount": customer_goal_obj.total_amount,
                    "customer_id": customer_goal_obj.customer_id.customer_id,
                    "customer_name": customer_goal_obj.customer_id.customer_name}
    customer_goal.update(plan)
    return customer_goal
