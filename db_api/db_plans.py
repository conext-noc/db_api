from db_api.models import Plans


# CREATE
def add_plan(plan_data):
    plan = Plans(**plan_data)
    plan.save()
    return {
        "plan": plan_data,
        "message": "Plan added successfully!",
    }


# READ
def get_plans():
    plans = Plans.objects.all().values()
    return {"message": "success", "data": list(plans)}


# UPDATE
def update_plan():
    return


# DELETE
def delete_plan():
    return
