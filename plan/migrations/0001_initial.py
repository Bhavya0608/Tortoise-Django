# Generated by Django 4.0.5 on 2022-06-26 06:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0002_rename_customers_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('plan_id', models.AutoField(primary_key=True, serialize=False)),
                ('plan_name', models.CharField(max_length=100)),
                ('benefit_per', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('benefit_type', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('promo_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('curr_user', models.IntegerField(default=0)),
                ('max_user', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('promo_per', models.IntegerField()),
                ('plan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.plan')),
            ],
        ),
        migrations.CreateModel(
            name='PlanOption',
            fields=[
                ('plan_option_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount_option', models.IntegerField()),
                ('tenure_option', models.IntegerField()),
                ('plan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.plan')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerGoal',
            fields=[
                ('customer_goal_id', models.AutoField(primary_key=True, serialize=False)),
                ('deposited_amount', models.IntegerField(default=0)),
                ('total_amount', models.IntegerField()),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('plan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.plan')),
                ('plan_option_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.planoption')),
                ('promo_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.promotion')),
            ],
        ),
    ]