"""BONUS: publish FreshCart-style web orders to the durable queue 'freshcart-orders'.

    python stream/bonus_publisher.py            # the same 5 orders every time (idempotency test)
    python stream/bonus_publisher.py --revise   # ORD-2003 again with a new amount and a later updated_at
"""
import argparse, json, os
import pika

QUEUE = "freshcart-orders"
ORDERS = [
    {"order_id": "ORD-2001", "cust_email": "priya.r@gmail.com", "cust_name": "Priya R", "order_date": "2026-09-02",
     "amount": "1,500.00", "currency": "INR", "pincode": "600041", "updated_at": "2026-09-02 10:00:00"},
    {"order_id": "ORD-2002", "cust_email": "arjun.k@yahoo.in", "cust_name": "Arjun K", "order_date": "2026-09-03",
     "amount": "20.00", "currency": "USD", "pincode": "560034", "updated_at": "2026-09-03 11:00:00"},
    {"order_id": "ORD-2003", "cust_email": "meera@outlook.com", "cust_name": "Meera S", "order_date": "2026-09-02",
     "amount": "2500", "currency": "INR", "pincode": "400050", "updated_at": "2026-09-02 12:00:00"},
    {"order_id": "ORD-2004", "cust_email": "priya.r@gmail.com", "cust_name": "Priya R", "order_date": "2026-09-03",
     "amount": "600", "currency": "inr", "pincode": "600041", "updated_at": "2026-09-03 13:00:00"},
    {"order_id": "ORD-2005", "cust_email": "arjun.k@yahoo.in", "cust_name": "Arjun K", "order_date": "2026-09-01",
     "amount": "10.00", "currency": "USD", "pincode": "560034", "updated_at": "2026-09-01 14:00:00"},
]

ap = argparse.ArgumentParser(); ap.add_argument("--revise", action="store_true"); a = ap.parse_args()
msgs = list(ORDERS)
if a.revise:
    msgs = [dict(ORDERS[2], amount="3000", updated_at="2026-09-04 09:00:00")]

conn = pika.BlockingConnection(pika.URLParameters(os.environ.get("AMQP_URL", "amqp://guest:guest@localhost:5672/%2F")))
ch = conn.channel(); ch.queue_declare(queue=QUEUE, durable=True)
for m in msgs:
    ch.basic_publish(exchange="", routing_key=QUEUE, body=json.dumps(m))
print(f"published {len(msgs)} orders to {QUEUE}")
conn.close()
