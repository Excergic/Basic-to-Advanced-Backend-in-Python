from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from backend.core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    instrument_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("instruments.id"))

    side: Mapped[str] = mapped_column(String(10))  # BUY/SELL
    order_type: Mapped[str] = mapped_column(String(20))  # LIMIT/MARKET
    price: Mapped[int] = mapped_column(Integer, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer)
    filled_quantity: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default="OPEN")
    leverage: Mapped[int] = mapped_column(Integer)
    margin_mode: Mapped[str] = mapped_column(String(20))  # CROSS/ISOLATED

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))