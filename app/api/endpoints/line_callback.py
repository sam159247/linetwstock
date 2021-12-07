from fastapi import APIRouter, HTTPException, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage
from loguru import logger

from app.core.config import settings
from app.internal.message_event import handle_message

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


router = APIRouter()


@router.post("/callback")
async def callback(request: Request) -> str:
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = await request.body()

    # handle webhook body
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError as e:
        logger.exception(e)
        raise HTTPException(
            status_code=400, detail="Invalid signature. Please check your channel access token/channel secret."
        )
    except LineBotApiError as e:
        logger.exception(f"LineBotApiError: {e.status_code} {e.message}")
        raise e

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event: MessageEvent) -> None:
    """Event - User sent message

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#message-event
    """
    handle_message(event=event)
