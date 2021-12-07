from linebot import LineBotApi
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from app.core.config import settings
from app.internal.finmind_api import FindMindAPI

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def handle_message(event: MessageEvent) -> None:
    """Event - User sent message

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#message-event
    """
    reply_token = event.reply_token
    if isinstance(event.message, TextMessage):
        input_text = event.message.text.split(" ")
        stock_id = input_text[0]
        start_date = input_text[1]
        end_date = ""
        if len(input_text) == 3:
            end_date = input_text[2]
        message = FindMindAPI.stock_price(stock_id, start_date, end_date)

        # Example to output raw data.
        messages = TextSendMessage(text=str(message))
        line_bot_api.reply_message(reply_token=reply_token, messages=messages)
