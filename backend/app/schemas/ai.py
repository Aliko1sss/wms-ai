from pydantic import BaseModel

class AIRequest(BaseModel):
    message: str
    confirm_action: bool = False

class AIResponse(BaseModel):
    response: str
    requires_confirm: bool = False