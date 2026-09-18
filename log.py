import logging

logging.basicConfig(
    filename="app.log",
    level="INFO",
    format="%(asctime)s--%(levelname)s -- %(message)s"
)

log=logging.getLogger("log")