from fastapi import APIRouter, Depends, HTTPException
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.ai import AIRequest, AIResponse
from app.services.ai import process_ai_query

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/chat", response_model=AIResponse)
def ai_chat(req: AIRequest, user: User = Depends(get_current_user)):
    if req.confirm_action:
        return AIResponse(response="Действие подтверждено. Задача отправлена в очередь обработки.", requires_confirm=False)
    result = process_ai_query(req.message, str(user.id))
    return AIResponse(**result)