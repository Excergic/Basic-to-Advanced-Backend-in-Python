from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    asset: Mapped[str] = mapped_column(String(20))
    balance: Mapped[int] = mapped_column(Integer)
    available_balance: Mapped[int] = mapped_column(Integer)

    user = relationship("User")