"""Driver: python stream/driver.py NAME PATTERN

Declares a private (exclusive, auto-delete) queue, binds it to the topic exchange with PATTERN,
prints each request and acknowledges it. A message with no 'zone' field is rejected with
basic_nack(requeue=False) (D3).

Optional flags for the D3 experiments:
    --requeue-bad        NACK bad messages with requeue=True (poison-message loop, Ctrl+C to stop)
    --crash-at N         exit WITHOUT acking the Nth message (shows redelivery)
"""
import argparse, json, os, sys

import pika

EXCHANGE = "rapido-dispatch"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("pattern")
    ap.add_argument("--requeue-bad", action="store_true")
    ap.add_argument("--crash-at", type=int, default=0)
    args = ap.parse_args()

    url = os.environ.get("AMQP_URL", "amqp://guest:guest@localhost:5672/%2F")
    conn = pika.BlockingConnection(pika.URLParameters(url))
    ch = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=False)
    queue = f"driver.{args.name}"
    ch.queue_declare(queue=queue, exclusive=True, auto_delete=True)   # private queue
    ch.queue_bind(queue=queue, exchange=EXCHANGE, routing_key=args.pattern)
    ch.basic_qos(prefetch_count=1)

    seen = {"n": 0}

    def on_message(channel, method, props, body):
        seen["n"] += 1
        tag = method.delivery_tag
        redelivered = " (REDELIVERED)" if method.redelivered else ""
        try:
            msg = json.loads(body)
        except json.JSONDecodeError:
            msg = {}
        if args.crash_at and seen["n"] == args.crash_at:
            print(f"[{args.name}] simulating crash before ACK of {method.routing_key}", flush=True)
            os._exit(1)
        if "zone" not in msg:
            print(f"[{args.name}] NACK (bad, dropped) key={method.routing_key}{redelivered} body={msg}", flush=True)
            channel.basic_nack(delivery_tag=tag, requeue=args.requeue_bad)
        else:
            print(f"[{args.name}] got key={method.routing_key:30s} id={msg['id']} zone={msg['zone']} "
                  f"type={msg['type']}{redelivered}", flush=True)
            channel.basic_ack(delivery_tag=tag)

    ch.basic_consume(queue=queue, on_message_callback=on_message, auto_ack=False)
    print(f"[{args.name}] waiting on {queue}, binding={args.pattern}", flush=True)
    try:
        ch.start_consuming()
    except KeyboardInterrupt:
        pass
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
