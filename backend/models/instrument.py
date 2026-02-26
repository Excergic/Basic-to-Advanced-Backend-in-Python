from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from backend.core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Instrument(Base):
    __tablename__ = "instruments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol: Mapped[str] = mapped_column(String(50), unique=True)
    contract_type: Mapped[str] = mapped_column(String(50))  # PERPETUAL
    tick_size: Mapped[int] = mapped_column(Integer)
    max_leverage: Mapped[int] = mapped_column(Integer)
    maintenance_margin_rate: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)