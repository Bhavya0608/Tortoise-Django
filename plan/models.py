from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from customer.models import Customer

# Create your models here.
class Plan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=100)
    benefit_per = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(0)])
    benefit_type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


class PlanOption(models.Model):
    plan_option_id = models.AutoField(primary_key=True)    
    amount_option = models.IntegerField()
    tenure_option = models.IntegerField()
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)


class Promotion(models.Model):
    promo_id = models.AutoField(primary_key=True)
    promo_name = models.CharField(max_length=100, unique=False)
    curr_user = models.IntegerField(default=0)
    max_user = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    promo_per = models.IntegerField()
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)


class CustomerGoal(models.Model):
    customer_goal_id = models.AutoField(primary_key=True)
    deposited_amount = models.IntegerField(default=0)
    total_amount = models.IntegerField()
    total_benefit = models.IntegerField(default=0, unique=False)
    start_date = models.DateField(unique=False)
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)
    plan_option_id = models.ForeignKey(PlanOption, on_delete=models.CASCADE)
    promo_id = models.ForeignKey(Promotion, on_delete=models.CASCADE, null=True, blank=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
