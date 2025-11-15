from sqlalchemy import Column, Integer, String, Float
from .database import Base


# SQLAlchemy ORM Models for existing Supabase tables
class TrailBalanceCurrentYear(Base):
    __tablename__ = "trial_balance_current_year"

    id = Column(Integer, primary_key=True, index=True)
    gl_account = Column(String, index=True)  # GL Account number
    account_name = Column(String, index=True)  # Account name
    debit = Column(Float, default=0.0)
    credit = Column(Float, default=0.0)
    balance = Column(Float, default=0.0)


class TrailBalancePreviousYear(Base):
    __tablename__ = "trial_balance_previous_year"

    id = Column(Integer, primary_key=True, index=True)
    gl_account = Column(String, index=True)  # GL Account number
    account_name = Column(String, index=True)  # Account name
    debit = Column(Float, default=0.0)
    credit = Column(Float, default=0.0)
    balance = Column(Float, default=0.0)