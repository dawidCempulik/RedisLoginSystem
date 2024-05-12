import redis
import os

redist_host = os.environ.get("REDIST_HOST")
redist_port = os.environ.get("REDIST_PORT")
redist_password = os.environ.get("REDIST_PASSWORD")

if redist_host is None or redist_port is None or redist_password is None:
    print("Environment variables not set. Aborting!")
    exit()


r = redis.Redis(
  host=redist_host,
  port=redist_port,
  password=redist_password,
  decode_responses=True)

r.set("foo", "bar")
print(r.get("foo"))
