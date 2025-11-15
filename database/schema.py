from pydantic import BaseModel, Field
from typing import List, Literal

# Base response model with common configuration
class ResponseBase(BaseModel):
    """Base class for all MCP tool responses"""
    class Config:
        from_attributes = True
        frozen = True  # Immutable responses

# Trail Balance Schemas
class TrailBalanceBase(ResponseBase):
    """Base trail balance data structure"""
    gl_account: str = Field(description="General ledger account code")
    account_name: str = Field(description="Account display name")
    debit: float = Field(description="Debit amount", ge=0)
    credit: float = Field(description="Credit amount", ge=0)
    balance: float = Field(description="Account balance")


# Tool Response Schemas
class TotalResponse(ResponseBase):
    """Response for column total calculations"""
    table_name: Literal['current_year', 'previous_year'] = Field(
        description="Source table"
    )
    column: Literal['debit', 'credit', 'balance'] = Field(
        description="Column that was totaled"
    )
    total: float = Field(description="Calculated sum", ge=0)


class AccountNamesResponse(ResponseBase):
    account_names: List[str]
    table_name: Literal['current_year', 'previous_year'] = Field(
        description="Source table"
    )

class GlAccountsResponse(ResponseBase):
    gl_accounts: List[str]
    table_name: Literal['current_year', 'previous_year'] = Field(
        description="Source table"
    )

class TotalMatchResponse(ResponseBase):
    debit_total: float
    credit_total: float
    is_balanced: bool
    table_name: Literal['current_year', 'previous_year'] = Field(
        description="Source table"
    )

class VarianceAnalysisItem(BaseModel):
    account_name: str
    current_balance: float
    previous_balance: float
    variance_amount: float
    variance_percentage: float
    exceeds_threshold: bool


class VarianceAnalysisResponse(ResponseBase):
    total_accounts: int
    variance_count: int
    threshold_used: float
    variances_exceeding_threshold: List[VarianceAnalysisItem]

