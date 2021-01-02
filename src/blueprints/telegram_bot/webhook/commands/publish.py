from flask import g, current_app

from src.api import telegram
from src.blueprints.telegram_bot._common.yandex_disk import (
    publish_item,
    get_element_info,
    YandexAPIGetElementInfoError,
    YandexAPIPublishItemError,
    YandexAPIRequestError
)
from src.blueprints.telegram_bot._common.stateful_chat import (
    stateful_chat_is_enabled,
    set_disposable_handler
)
from src.blueprints.telegram_bot._common.command_names import (
    CommandName
)
from src.blueprints.telegram_bot.webhook.dispatcher_interface import (
    DispatcherEvent
)
from ._common.responses import (
    cancel_command,
    request_absolute_path,
    send_yandex_disk_error
)
from ._common.decorators import (
    yd_access_token_required,
    get_db_data
)
from ._common.utils import (
    extract_absolute_path,
    create_element_info_html_text
)


@yd_access_token_required
@get_db_data
def handle(*args, **kwargs):
    """
    Handles `/publish` command.
    """
    message = kwargs.get(
        "message",
        g.telegram_message
    )
    user_id = kwargs.get(
        "user_id",
        g.telegram_user.id
    )
    chat_id = kwargs.get(
        "chat_id",
        g.telegram_chat.id
    )
    path = extract_absolute_path(
        message,
        CommandName.PUBLISH.value,
        kwargs.get("route_source")
    )

    if not path:
        if stateful_chat_is_enabled():
            set_disposable_handler(
                user_id,
                chat_id,
                CommandName.PUBLISH.value,
                [
                    DispatcherEvent.PLAIN_TEXT.value,
                    DispatcherEvent.BOT_COMMAND.value,
                    DispatcherEvent.EMAIL.value,
                    DispatcherEvent.HASHTAG.value,
                    DispatcherEvent.URL.value
                ],
                current_app.config["RUNTIME_DISPOSABLE_HANDLER_EXPIRE"]
            )

        return request_absolute_path(chat_id)

    user = g.db_user
    access_token = user.yandex_disk_token.get_access_token()

    try:
        publish_item(access_token, path)
    except YandexAPIRequestError as error:
        cancel_command(chat_id)
        raise error
    except YandexAPIPublishItemError as error:
        send_yandex_disk_error(chat_id, str(error))

        # it is expected error and should be
        # logged only to user
        return

    info = None

    try:
        info = get_element_info(access_token, path)
    except YandexAPIRequestError as error:
        cancel_command(chat_id)
        raise error
    except YandexAPIGetElementInfoError as error:
        send_yandex_disk_error(chat_id, str(error))

        # it is expected error and should be
        # logged only to user
        return

    text = create_element_info_html_text(info, False)

    telegram.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode="HTML",
        disable_web_page_preview=True
    )
