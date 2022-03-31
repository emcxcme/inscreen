from telegram import Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, Filters, MessageHandler
from app.chat.message.template import greet_user
from app.config import CONFIG
from app.configs import ADMIN_IDS, INSCREEN_HELPER_IDS, INSCREEN_ID, INSCREEN_USERNAME


def greet_new_member(update: Update, context: CallbackContext) -> None:
    user = update.message.new_chat_members[0]
    if user.id == CONFIG[INSCREEN_ID]:
        text = (
            "Salamat po sa pag-add sa akin dito."
            " Kailangan po munang ma-convert itong group sa supergroup"
            " at ma-issue ang /register command bago po ito tuluyang magamit."
            " Maanong paki bigyan na rin po ako ng full admin rights"
            " maliban po sa <b>Remain Anonymous</b>"
        )
        update.message.reply_text(text, "html")
        return
    if user.id in CONFIG[ADMIN_IDS] or user.id in CONFIG[INSCREEN_HELPER_IDS]:
        chat = update.message.chat
        try:
            update.message.bot.promote_chat_member(
                chat.id,
                user.id,
                can_change_info=True,
                can_delete_messages=True,
                can_restrict_members=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_manage_voice_chats=True,
                can_promote_members=True,
                is_anonymous=False,
                can_manage_chat=True,
            )
        except BadRequest:
            text = (
                "I'm unable to promote <a href='tg://user?id=%s'>%s</a>."
                " Please give me <b>Add New Admins</b> right."
                % (user.id, user.first_name,)
            )
            update.message.reply_text(text, "html")
            return
        text = "<a href='tg://user?id=%s'>%s</a> promoted as admin." % (
            user.id,
            user.first_name,
        )
        update.message.reply_text(text, "html")
        return
    text = (
        greet_user(user.id, user.first_name)
        + " Pumunta po muna kayo rito sa @%s at mag-register bago po mag-send ng screenshot."
        % CONFIG[INSCREEN_USERNAME]
    )
    update.message.reply_text(text, "html")
    return


handler = MessageHandler(Filters.status_update.new_chat_members, greet_new_member)
