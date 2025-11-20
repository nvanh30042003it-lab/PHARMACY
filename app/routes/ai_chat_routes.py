from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
import os

router = APIRouter(prefix="/ai", tags=["AI Chat"])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

SYSTEM_PROMPT = """
Bạn là chatbot tư vấn thuốc cho Nhà Thuốc ANHDUONG.
Bạn trả lời lịch sự, rõ ràng, ngắn gọn nhưng hữu ích.
Không đưa lời khuyên y tế chuyên sâu. Gợi ý sản phẩm nếu phù hợp.
"""

@router.post("/chat")
def chat_ai(req: ChatRequest):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req.message},
        ],
    )
    # `message` is a ChatCompletionMessage object; access `.content` attribute.
    reply = None
    if response.choices:
        # Some SDK versions return a ChatCompletionMessage object with `.content`.
        msg = response.choices[0].message
        reply = getattr(msg, "content", None) or (msg.get("content") if isinstance(msg, dict) else None)

    return {"reply": reply}
