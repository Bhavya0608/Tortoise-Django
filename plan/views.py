from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

from .models import CustomerGoal, Plan, PlanOption, Promotion
from customer.models import Customer
from . import scripts as func


# Create your views here.
def create_plan(request):
    p = Plan(plan_name = request.GET.get("plan_name"), benefit_per = request.GET.get("benefit_per"), benefit_type = request.GET.get("benefit_type"))
    p.save()
    amount_option = [int(i.strip()) for i in request.GET.get("amount_option").split(",")]
    tenure_option = [int(i.strip()) for i in request.GET.get("tenure_option").split(",")]
    for i in range(len(amount_option)):
        po = PlanOption(amount_option=amount_option[i], tenure_option=tenure_option[i], plan_id=p)
        po.save()
    return JsonResponse({"plans": func.plan_from_id(p.plan_id)})   


def get_plans(request):
    return JsonResponse({"plans": func.get_all_plans()})


def create_promotion(request):
    plan_id = request.GET.get("plan_id")
    print(datetime.strptime(request.GET.get("start_date"), "%d-%m-%Y").date())
    pr = Promotion(promo_name=request.GET.get("promo_name"),
                    max_user=int(request.GET.get("max_user")),
                    start_date=datetime.strptime(request.GET.get("start_date"), "%d-%m-%Y").date(), 
                    end_date=datetime.strptime(request.GET.get("end_date"), "%d-%m-%Y").date(),
                    promo_per=request.GET.get("promo_per"), 
                    plan_id=Plan.objects.get(plan_id=plan_id))
    pr.save()
    return JsonResponse({"promotion": {"promotion_id": pr.promo_id, "msg": "promotion saved"}})


def promotions_for_plan(request):
    plan_id = request.GET.get("plan_id")
    return JsonResponse({"promotions for plan id={}".format(plan_id) : func.promotions_from_id(plan_id=plan_id)})


def create_customer_goal(request):
    plan_id = request.GET.get("plan_id")
    plan_option_id = request.GET.get("plan_option_id")
    promo_id = request.GET.get("promo_id", None)
    customer_id = request.GET.get("customer_id")
    plan = func.plan_from_id(plan_id=plan_id, plan_object_id=plan_option_id)[0]
    total_amount = plan["amount_option"] * plan["tenure_option"]
    promo = Promotion.objects.get(promo_id=promo_id) if promo_id else None
    total_benefit = min(plan["benefit_per"] + (promo.promo_per if promo else 0), 100)
    cg = CustomerGoal(total_amount=total_amount, 
                        total_benefit=total_benefit, 
                        plan_id=Plan.objects.get(plan_id=plan_id),
                        start_date = datetime.now().date(),
                        plan_option_id=PlanOption.objects.get(plan_option_id=plan_option_id), 
                        promo_id=promo, 
                        customer_id=Customer.objects.get(customer_id=customer_id))
    cg.save()
    if promo:
        func.use_promotion(promo_id=promo.promo_id)
    return JsonResponse({"Customer goal saved with customer_goal_id" : cg.customer_goal_id})


def get_customer_goal(request):
    return JsonResponse({"Customer Goal Details" : func.get_customer_goal_from_id(request.GET.get("customer_goal_id"))})
