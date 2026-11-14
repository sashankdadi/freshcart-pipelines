"""Dispatcher: publishes a ride/food request every N seconds to the topic exchange 'rapido-dispatch'.

    python stream/dispatcher.py                         # run until Ctrl+C
    python stream/dispatcher.py --duration 120          # run for two minutes (D2)
    python stream/dispatcher.py --duration 120 --bad-every 10   # every 10th message lacks 'zone' (D3)

Broker URL comes from the AMQP_URL environment variable (never hard-code it).
"""
import argparse, json, os, random, time, uuid
from datetime import datetime, timezone

import pika

EXCHANGE = "rapido-dispatch"
ZONES = {"bangalore": ["koramangala", "indiranagar", "whitefield"],
         "chennai": ["tnagar", "whitefield", "adyar"]}
TYPES = ["ride", "food"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval", type=float, default=2.0, help="seconds between messages")
    ap.add_argument("--duration", type=float, default=0, help="stop after N seconds (0 = forever)")
    ap.add_argument("--bad-every", type=int, default=0, help="every Nth message is missing 'zone' (0 = never)")
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()
    if args.seed is not None:
        random.seed(args.seed)

    url = os.environ.get("AMQP_URL", "amqp://guest:guest@localhost:5672/%2F")
    conn = pika.BlockingConnection(pika.URLParameters(url))
    ch = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=False)

    start, n = time.time(), 0
    try:
        while args.duration == 0 or time.time() - start < args.duration:
            n += 1
            city = random.choice(list(ZONES))
            zone = random.choice(ZONES[city])
            typ = random.choice(TYPES)
            key = f"{city}.{zone}.{typ}"
            msg = {"id": str(uuid.uuid4())[:8], "city": city, "zone": zone, "type": typ,
                   "ts": datetime.now(timezone.utc).isoformat()}
            bad = args.bad_every and n % args.bad_every == 0
            if bad:
                del msg["zone"]                       # D3: a malformed message (routing key is still fine)
            ch.basic_publish(exchange=EXCHANGE, routing_key=key, body=json.dumps(msg))
            print(f"[{n:03d}] published key={key:32s} id={msg['id']}{'  <-- BAD (no zone)' if bad else ''}", flush=True)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        pass
    finally:
        conn.close()
        print(f"dispatcher stopped after {n} messages")


if __name__ == "__main__":
    main()
