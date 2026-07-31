from pydantic import BaseModel


class CitizenSignup(BaseModel):
    name: str
    phone: str
    password: str


class CitizenLogin(BaseModel):
    phone: str
    password: str


class OfficerLogin(BaseModel):
    employee_id: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str | None = None
    ward: str | None = None
    user: dict | None = None
