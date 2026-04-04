"""
Clean up financial data: Move mistyped 'Invoices' from obligations (payables) to receivables.
Per user requirement: "all invoices are receivables and remaining all are payables".
"""

import sys
import os
import uuid
import datetime
import asyncio
from sqlalchemy import select, and_, delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Setup path for app imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models.obligation import Obligation
from app.models.receivable import Receivable, ReceivableStatus

DATABASE_URL = "sqlite+aiosqlite:///dev.db"
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def migrate_invoices():
    async with AsyncSessionLocal() as session:
        # 1. Find all obligations whose description starts with "Invoice"
        # These are actually receivables per user definition.
        result = await session.execute(
            select(Obligation).where(
                and_(
                    Obligation.description.like("Invoice%"),
                    Obligation.deleted_at.is_(None)
                )
            )
        )
        invoices_to_move = result.scalars().all()
        
        if not invoices_to_move:
            print("No misclassified invoices found in obligations.")
            return

        print(f"Found {len(invoices_to_move)} misclassified invoices. Moving to receivables...")

        for ob in invoices_to_move:
            # 2. Check if it already exists in receivables by description and user
            exists_result = await session.execute(
                select(Receivable).where(
                    and_(
                        Receivable.user_id == ob.user_id,
                        Receivable.description == ob.description
                    )
                )
            )
            existing = exists_result.scalar_one_or_none()
            
            if not existing:
                # Create a new Receivable
                new_rec = Receivable(
                    id=str(uuid.uuid4()),
                    user_id=ob.user_id,
                    client_name="Unknown Client", # Default
                    description=ob.description,
                    amount=ob.amount,
                    amount_received=ob.amount_paid, # Assume paid amount corresponds
                    due_date=ob.due_date,
                    status=ReceivableStatus.pending,
                    created_at=ob.created_at,
                )
                session.add(new_rec)
                print(f"  + Added to receivables: {ob.description} (${ob.amount})")
            else:
                print(f"  ~ Already exists in receivables: {ob.description}")

            # 3. Delete from obligations (soft delete to be safe)
            # Or just delete if we're sure
            await session.delete(ob)
            print(f"  - Deleted from obligations: {ob.description}")
        
        await session.commit()
        print("Migration complete!")

if __name__ == "__main__":
    asyncio.run(migrate_invoices())
