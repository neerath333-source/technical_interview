from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError
from ..patterns import PATTERN_UPPERCASE, PATTERN_LOWERCASE, PATTERN_NUMBER, PATTERN_SPECIAL_CHAR, PATTERN_NAME, PATTERN_EMAIL

class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    password: str = Field(..., min_length=8)
    tenant_name: str = Field(..., min_length=2)

    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        if not PATTERN_EMAIL.match(v):
            raise ValueError('Invalid email format or contains uppercase letters (must be lowercase)')
        return v

    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        if not PATTERN_UPPERCASE.search(v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not PATTERN_LOWERCASE.search(v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not PATTERN_NUMBER.search(v):
            raise ValueError('Password must contain at least one number')
        if not PATTERN_SPECIAL_CHAR.search(v):
            raise ValueError('Password must contain at least one special character (@$!%*#?&)')
        return v

    @field_validator('tenant_name')
    @classmethod
    def validate_tenant_name(cls, v: str) -> str:
        if not PATTERN_NAME.match(v):
            raise ValueError('Tenant Name must contain only characters (no numbers or special characters allowed)')
        return v

class UserLoginSchema(BaseModel):
    email: str
    password: str

    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        if not PATTERN_EMAIL.match(v):
            raise ValueError('Invalid email format')
        return v
