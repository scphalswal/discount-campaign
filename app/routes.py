from fastapi import APIRouter, HTTPException
from app.models import Campaign, Customer, Order
from app.utils import read_file, write_file, convert_datetime
from typing import List
from datetime import datetime, date
from logging import getLogger

log = getLogger(__name__)
router = APIRouter()

CAMPAIGN_FILE  = 'app/campaign_data.json'
USER_FILE = 'app/user_data.json'
ORDER_FILE = 'app/order_data.json'

# ----------------- Campaign APIs -----------------

@router.get("/campaigns", response_model=List[Campaign])
def list_campaigns():
    return read_file(CAMPAIGN_FILE)

@router.post("/campaigns", status_code=201)
def create_campaign(campaign: Campaign):
    campaigns = read_file(CAMPAIGN_FILE)

    if any(camp["id"] == campaign.id for camp in campaigns):
        raise HTTPException(status_code=409, detail="Campaign with this ID already exists.")

    campaigns.append(dict(campaign))
    write_file(campaigns, CAMPAIGN_FILE)
    return {"message": "Campaign created successfully."}

@router.get("/campaigns/{campaign_id}", response_model=Campaign)
def get_campaign(campaign_id: int):
    campaigns = read_file(CAMPAIGN_FILE)
    for campaign in campaigns:
        if campaign["id"] == campaign_id:
            return campaign
    raise HTTPException(status_code=404, detail="Campaign not found.")

@router.put("/campaigns/{campaign_id}")
def update_campaign(campaign_id: int, updated_data: Campaign):
    campaigns = read_file(CAMPAIGN_FILE)
    for index, campaign in enumerate(campaigns):
        if campaign["id"] == campaign_id:
            campaigns[index] = updated_data.dict()
            write_file(campaigns, CAMPAIGN_FILE)
            return {"message": "Campaign updated successfully."}
    raise HTTPException(status_code=404, detail="Campaign not found.")

@router.delete("/campaigns/{campaign_id}")
def delete_campaign(campaign_id: int):
    campaigns = read_file(CAMPAIGN_FILE)
    updated_campaigns = [c for c in campaigns if c["id"] != campaign_id]
    if len(updated_campaigns) == len(campaigns):
        raise HTTPException(status_code=404, detail="Campaign not found.")
    write_file(updated_campaigns, CAMPAIGN_FILE)
    return {"message": "Campaign deleted successfully."}




# ----------------- User APIs -----------------

@router.post("/users/", response_model=Customer)
def create_user(user: Customer):
    users = read_file(USER_FILE)
    if any(u['id'] == user.id and u['email'] == user.email for u in users):
        raise HTTPException(status_code=400, detail="User already exists.")
    users.append(dict(user))
    write_file(users, USER_FILE)
    return user


@router.get("/users/{user_id}", response_model=Customer)
def get_user(user_id: int):
    users = read_file(USER_FILE)
    for user in users:
        if user['id'] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@router.put("/users/{user_id}", response_model=Customer)
def update_user(user_id: int, updated_data: Customer):
    users = read_file(USER_FILE)
    for index, u in enumerate(users):
        if u['id'] == user_id:
            updated_data.updated_at = datetime.utcnow()
            users[index] = updated_data.dict()
            write_file(users, USER_FILE)
            return updated_data
    raise HTTPException(status_code=404, detail="User not found")


@router.post("create_order/")
def create_order(order: Order):
    """
        Create an order and apply campaign discount if:
        - The user is eligible
        - The order limit per day is not exceeded
        - The campaign is still active and has balance
    """

    orders = read_file(ORDER_FILE)
    user_id = order.user_id
    campaign_id = order.campaign_id
    total_cart_amount = order.total_cart_amount

    if any(ord["id"] == order.id for ord in orders):
        raise HTTPException(status_code=409, detail="Campaign with this ID already exists.")

    # check if user applicable for the discount
    users = read_file(USER_FILE)
    order_dict = dict(order)
    user = None
    for u in users:
        if u['id'] == user_id:
            user = u
            break

    if not user:
        log.error("User not found")
        raise HTTPException(status_code=404, detail="User not found")

    if not user['discount_available']:
        log.info("User is not eligible for discounts.")
        orders.append(order_dict)
        write_file(orders, ORDER_FILE)
        order_dict['discount_details'] = f'You are not eligible for discounts.'
        return order_dict


    # check if user has exceeded the maximum transactions per day
    order_created_per_day = sum(
        1 for o in orders if o['user_id'] == user_id and o['created_at'] == str(date.today())
    )
    print(order_created_per_day,'order_created_per_day')
    if order_created_per_day >= 3:
        log.info("User has exceeded the max transactions per day.")
        orders.append(order_dict)
        write_file(orders, ORDER_FILE)
        order_dict['discount_details'] = 'You are not eligible for discounts as your max order limit exceeded.'
        return order_dict


    campaign_details = read_file(CAMPAIGN_FILE)

    discount_amount = 0
    for c in campaign_details:
        if c['id'] == campaign_id:
            discount_percentage = c['discount_percentage']
            discount_amount = total_cart_amount - (total_cart_amount * discount_percentage / 100)
            if c['campaign_amount'] < discount_amount:
                orders.append(order_dict)
                write_file(orders, ORDER_FILE)
                order_dict['discount_details'] = f'Now sale is end'
                return order_dict
            c['campaign_amount'] -= discount_amount
            write_file(campaign_details, CAMPAIGN_FILE)
            break

    order_dict = dict(order)
    order_dict['discount_details'] = discount_amount
    orders.append(order_dict)
    write_file(orders, ORDER_FILE)
    return order_dict





