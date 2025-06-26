import logging

logging.basicConfig(
    filename="escola_infantil.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)