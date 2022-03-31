import logging
from telegram.ext import PicklePersistence, Updater
from app.config import CONFIG
from app.configs import APP_PERSISTENCE_FILE, INSCREEN_TOKEN
from app.handlers import (
    forward,
    group_registration,
    help,
    image_reception,
    new_member,
    start,
    text_reception,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def main() -> None:
    pickle_persistence = PicklePersistence(CONFIG[APP_PERSISTENCE_FILE])
    updater = Updater(CONFIG[INSCREEN_TOKEN], persistence=pickle_persistence)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(forward.handler)
    dispatcher.add_handler(group_registration.handler)
    dispatcher.add_handler(image_reception.handler)
    dispatcher.add_handler(new_member.handler)
    dispatcher.add_handler(start.handler)
    dispatcher.add_handler(text_reception.handler)
    updater.start_polling()
    updater.idle()
