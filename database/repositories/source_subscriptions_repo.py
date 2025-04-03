from sqlalchemy.future import select
from database.models import SourcesSubscription
from database.session import Database, db


class SourcesSubscriptionRepository:
    def __init__(self, db: Database):
        self.db = db


    async def create_subscription(self,
                                   telegram_id: int,
                                   source_id: int,
                                   ) -> None:
        async with self.db.session() as session:
            subscription = SourcesSubscription(
                                            telegram_id=telegram_id,
                                            source_id=source_id,
                                            )
            session.add(subscription)
            await session.commit()


    async def delete_subscription(self,
                                  telegram_id: int,
                                  source_id: int,
                                  ) -> None:
        async with self.db.session() as session:
            subscription_to_delete = await session.execute(
                select(SourcesSubscription).filter(
                    SourcesSubscription.telegram_id == telegram_id,
                    SourcesSubscription.source_id == source_id))
            subscription_to_delete = subscription_to_delete.scalars().first()

            if subscription_to_delete:
                await session.delete(subscription_to_delete)
                await session.commit()


    async def is_subscription(self,
                                telegram_id: int,
                                source_id: int,
                                ) -> bool:
        async with self.db.session() as session:
            subscription = await session.execute(
                select(SourcesSubscription).filter(
                    SourcesSubscription.telegram_id == telegram_id,
                    SourcesSubscription.source_id == source_id))
            result = subscription.scalars().first()
            if result:
                return True
            else:
                return False


    async def get_users_and_subscriptions(self):
        user_subscriptions = []

        async with self.db.session() as session:
            stmt = select(SourcesSubscription.telegram_id, SourcesSubscription.source_id)
            response = await session.execute(stmt)
            subscriptions_dict = {}

            for telegram_id, source_id in response.all():
                if telegram_id not in subscriptions_dict:
                    subscriptions_dict[telegram_id] = []
                subscriptions_dict[telegram_id].append(source_id)

            # Преобразуем в список словарей в нужном формате
            for telegram_id, source_ids in subscriptions_dict.items():
                user_subscriptions.append({
                    'telegram_id': telegram_id,
                    'source_id': source_ids
                })

        return user_subscriptions



sources_subscriptions = SourcesSubscriptionRepository(db)
