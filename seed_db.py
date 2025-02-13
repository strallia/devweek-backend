from app import app, db, User, Group, Event, Expense, ExpenseSplit, Notification, DiscussionThread, Message, user_group, user_event
from datetime import datetime

with app.app_context():
    print("Seeding database...")

    # Seed User
    users = [
        User(
            id=1,
            user_icon=None,
            username="JohnGarcia",
            email="john.garcia@example.com",
            password_hash="scrypt:32768:8:1$6hJCKBk3ryC0LFyj$c30901fb6a99a50cae7adf7203872d0974da3b95a48b04595c0dc33c28102bfef8bd54986a2291f56a38404575b0366b4d65cc4adaf6b73e4507cd329edb0500",
            created_at="2025-02-13 03:28:02.638014",
            updated_at="2025-02-13 03:28:02.638014"
        ),
        User(
            id=2,
            user_icon=None,
            username="Ana Taylor",
            email="ataylor@example.com",
            password_hash="scrypt:32768:8:1$bYXrOeIGsWDMzTA3$536735400fc093e05a1dbf79632459ccfa38d3fc27f95cbf9b67f78e088672f015e348786e623c7ef8a7ba01c4b45d2385ed69392c0390dd768058223ae6926c",
            created_at="2025-02-13 03:28:02.638014",
            updated_at="2025-02-13 03:28:02.638014"
        ),
        User(
            id=3,
            user_icon=None,
            username="Maximillion",
            email="maximillion@example.com",
            password_hash="scrypt:32768:8:1$h7RnRUUnVHxrebXk$42969223e7e7550b1791958dffdef78591356fc7acb13f0fde004fa64bd97d6f9208263d86970c8feb1b5d69affd5cd026729c699cc890c37fb9d6e270efc854",
            created_at="2025-02-13 03:28:02.638014",
            updated_at="2025-02-13 03:28:02.638014"
        ),
        User(
            id=4,
            user_icon=None,
            username="Roger Martin",
            email="rmartin@example.com",
            password_hash="scrypt:32768:8:1$lJI4WdKKrtvDuGcG$d339df7ce01acd3a0bd027761162520a1768bf37e71fe0de9688aff705ed0b56939e8e494696d049dc420ebd1b4837a22e8bb30ec23c7cf1a303cf676bc48388",
            created_at="2025-02-13 03:28:02.638014",
            updated_at="2025-02-13 03:28:02.638014"
        ),
        User(
            id=5,
            user_icon=None,
            username="Lydia",
            email="lydia@example.com",
            password_hash="scrypt:32768:8:1$OsgsRGfq49MDaNbY$c5662853f52c71d45aa8fc5be69439dcb71b67cd1e19236b468790cb1ee8654f0fa60754314073c3b0cbf1709533fce290f39f4cbcc5e3bf8bfb93966b36ab1f",
            created_at="2025-02-13 03:28:02.638014",
            updated_at="2025-02-13 03:28:02.638014"
        ),
        User(
            id=6,
            user_icon=None,
            username="Amanda P",
            email="amandap@example.com",
            password_hash="scrypt:32768:8:1$auTr9khLNUTgwWX9$fc8167e67b66f6705a3b5cf55f9544f1c151ab852dac052816feb1f5b28235e333dea3d66764e3610e8f48685dcf647216fd5ec5b99ef174741a673a9814dffb",
            created_at="2025-02-13 03:28:02.638014",
            updated_at="2025-02-13 03:28:02.638014"
        ),
        User(
            id=7,
            user_icon=None,
            username="Coolguy",
            email="coolguy@example.com",
            password_hash="scrypt:32768:8:1$Xz7cgCouICnv3T3H$16e39da128ca5c38ea643e66c3b25280980ce324df81852259e72f63aca425208d11e92c7d884c6c11d83e55e3dc71c17a64f977815ce7de90a31ea37ac699e6",
            created_at="2025-02-13 03:28:02.638014",
            updated_at="2025-02-13 03:28:02.638014"
        ),
        User(
            id=8,
            user_icon=None,
            username="Martina",
            email="martina@example.com",
            password_hash="scrypt:32768:8:1$7nTpW2T7DB6xio6O$826679d090f74a0dd8cf21ec7e0cbbaf406a76a075b466abc1c07883233921957277e0a9337250ada4091e7325af7d1aa12c3f4e8e197c6ef1d7cad1c89f866d",
            created_at="2025-02-13 03:28:02.638014",
            updated_at="2025-02-13 03:28:02.638014"
        ),
        User(
            id=9,
            user_icon=None,
            username="Khushnood",
            email="khushnood@example.com",
            password_hash="scrypt:32768:8:1$nEX1UN4qnzM9PhSI$fb1b84035b3412f9644fad19b6903eec75d56f0ddfee1c689885e5f7d196db80b94b54c2fc31838c96e8a29dc5486b460e59038a7a03f008cc5422e6fc348150",
            created_at="2025-02-13 03:28:02.638014",
            updated_at="2025-02-13 03:28:02.638014"
        ),
        User(
            id=10,
            user_icon=None,
            username="Pegasus",
            email="pegasus@example.com",
            password_hash="scrypt:32768:8:1$jQyaygMqfIE3tIXT$03bebbf8d94fea8da3f4b954834a229926c89a13c8e98a9ca9c1a83d17d302c144e9e7f027f6eb3b0d1e7a947726785a39c67562b5b5802fa3020c510b3d4f1e",
            created_at="2025-02-13 03:28:02.638014",
            updated_at="2025-02-13 03:28:02.638014"
        )
    ]
    db.session.add_all(users)

    # Seed Group
    groups = [
        Group(
            id=1,
            group_icon=None,
            group_name="Book Club",
            description="Group for a book club",
            created_at="2025-02-13 03:28:02.640011",
            updated_at="2025-02-13 03:28:02.640011"
        ),
        Group(
            id=2,
            group_icon=None,
            group_name="Coding Buddies",
            description="Group for good code",
            created_at="2025-02-13 03:28:02.640011",
            updated_at="2025-02-13 03:28:02.640011"
        ),
        Group(
            id=3,
            group_icon=None,
            group_name="FastTourists",
            description="Group for tourism",
            created_at="2025-02-13 03:28:02.640011",
            updated_at="2025-02-13 03:28:02.640011"
        )
    ]
    db.session.add_all(groups)

    # Seed Expense
    expenses = [
        Expense(
            id=1,
            description="Expense 1",
            amount=62.5,
            amount_paid=62.5,
            amount_remaining=0,
            currency="USD",
            event_id=1,
            user_id=1,
            created_at="2025-02-13 03:28:02.641011",
            updated_at="2025-02-13 03:28:02.641011"
        ),
        Expense(
            id=2,
            description="Expense 2",
            amount=62.5,
            amount_paid=62.5,
            amount_remaining=0,
            currency="USD",
            event_id=1,
            user_id=2,
            created_at="2025-02-13 03:28:02.641011",
            updated_at="2025-02-13 03:28:02.641011"
        )
    ]
    db.session.add_all(expenses)

    # Seed ExpenseSplit
    expense_splits = [
        ExpenseSplit(
            id=1,
            amount_owed=62.5,
            amount_paid=62.5,
            algorithm_used="equally",
            user_id=1,
            expense_id=1
        ),
        ExpenseSplit(
            id=2,
            amount_owed=62.5,
            amount_paid=0,
            algorithm_used="equally",
            user_id=2,
            expense_id=1
        )
    ]
    db.session.add_all(expense_splits)

    # Seed Event
    events = [
        Event(
            id=1,
            event_name="Book Festival",
            event_icon=None,
            description="The greatest book festival of the year",
            event_type="Festival",
            cost_to_attend=None,
            location="Santa Clara",
            date=datetime(2025, 6, 15, 11, 0, 0),
            photos=None,
            visibility="Public",
            category="Category1",
            group_id=1,
            created_at="2025-02-13 03:28:02.641011",
            updated_at="2025-02-13 03:28:02.641011"
        ),
        Event(
            id=2,
            event_name="2025 Hackathon",
            event_icon=None,
            description="The greatest Hackathon of the year",
            event_type="Hackathon",
            cost_to_attend=None,
            location="Santa Clara",
            date=datetime(2025, 6, 15, 11, 0, 0),
            photos=None,
            visibility="Public",
            category="Category2",
            group_id=2,
            created_at="2025-02-13 03:28:02.641011",
            updated_at="2025-02-13 03:28:02.641011"
        )
    ]
    db.session.add_all(events)

    # Commit table data to make sure they exist in the database
    db.session.commit()

    # Seed user_group many to many relationship table
    user_group_data = [
        {'user_id': 1, 'group_id': 1}, 
        {'user_id': 2, 'group_id': 1}, 
        {'user_id': 3, 'group_id': 1},
        {'user_id': 4, 'group_id': 1},
        {'user_id': 1, 'group_id': 3},
        {'user_id': 3, 'group_id': 3},
        {'user_id': 5, 'group_id': 3},
        {'user_id': 7, 'group_id': 3},
        {'user_id': 9, 'group_id': 3},
    ]
    for row in user_group_data:
        db.session.execute(user_group.insert().values(row))

    # Seed user_event many to many relationship table
    user_event_data = [
        {'user_id': 3, 'event_id': 1}, 
        {'user_id': 4, 'event_id': 1}, 
        {'user_id': 5, 'event_id': 1},
        {'user_id': 6, 'event_id': 1},
        {'user_id': 7, 'event_id': 2},
        {'user_id': 6, 'event_id': 2},
        {'user_id': 5, 'event_id': 2},
    ]
    for row in user_event_data:
        db.session.execute(user_event.insert().values(row))

    # Commit the many-to-many relationship tables
    db.session.commit()

    print("Database seeding complete")