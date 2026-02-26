from sqlalchemy import Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from backend.core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instrument_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("instruments.id"))
    buy_order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id"))
    sell_order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id"))

    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer)
    taker_side: Mapped[str] = mapped_column(String(10))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))