from pydantic import BaseModel
from typing import Optional

class UserModel(BaseModel):
    user_name: str
    password_hash: str
    role_id: Optional[int] = None
    
    model_config = {"from_attributes": True}