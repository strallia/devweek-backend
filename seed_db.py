from app import app, db, User, Group, Event, Expense, ExpenseSplit, Notification, DiscussionThread, Message, user_group

with app.app_context():
    print("Seeding database...")

    # Seed User
    users = [
        User(
            id=3,
            user_icon=None,
            username="John Wick",
            email="johnwick2@gmail.com",
            password_hash="scrypt:32768:8:1$J2DM7AwQeyCBhyxd$2859ebac445a1d856a98aa16261898f2b6226ed437c45abe9d1a19435ff914ccba24b39eedc36ef9c715e6381e639799b826a65bd7eda97753fb0d9e190e074c",
            created_at="2025-02-08 16:56:14.934472",
            updated_at="2025-02-08 16:56:14.934472"
        ),
        User(
            id=4,
            user_icon=None,
            username="Ron Weasley",
            email="ronwsley@gmail.com",
            password_hash="scrypt:32768:8:1$0EyUTJBvnxQTbGrC$4cd9a25a2e554b565676b3a78fbd17eadb5f85bd7ce24a6c3f478b1938f545d04c5b73bd5bf90a8cfa4f291043d022afbbac19e5c8f5211f71dcd36f895512da",
            created_at="2025-02-08 21:23:44.224368",
            updated_at="2025-02-08 21:23:44.224368"
        ),
        User(
            id=5,
            user_icon=None,
            username="Maximillion",
            email="maximillion@gmail.com",
            password_hash="scrypt:32768:8:1$FCrBGhCduSphozFH$6655b236b3da26df8c980e73a86bcf032af942cb4dead27077298fa52b61f19d1163846231e355f00cc9163514e155dd812482550b8e4518403f3674ae6687eb",
            created_at="2025-02-08 21:23:44.224368",
            updated_at="2025-02-08 21:23:44.224368"
        ),
        User(
            id=6,
            user_icon=None,
            username="Pegasus",
            email="pegasus@gmail.com",
            password_hash="scrypt:32768:8:1$rqXGeBqUBDOMqw3x$e3220ec50a60dd697bc7f308aeb596f6ed3b8db29728ab7bbdbfbd42d98bfa3fae3d780eb511fba3ff7c7f0f7de9c0c356b5c6715dfec8ed7c31bece8c8d5eb2",
            created_at="2025-02-08 22:34:41.95621",
            updated_at="2025-02-08 22:34:41.95621"
        ),
        User(
            id=7,
            user_icon=None,
            username="Pegasus24",
            email="pegasus24@gmail.com",
            password_hash="scrypt:32768:8:1$krWGpWiT1kFw1a86$c6d1e02212d29e2af2d6ae786b683989787ff2b5698e9865d1f8f3e2452e3349d79ceb366da0dbcfa390ce24c7c9a5062df80fc016fdc1508a192b089a96401d",
            created_at="2025-02-11 00:47:16.105439",
            updated_at="2025-02-11 00:47:16.105439"
        )
    ]
    db.session.add_all(users)
    
    # Seed Group
    groups = [
        Group(
            id=1,
            group_icon=None,
            group_name="Group1",
            description="A test group",
            created_at="2025-02-08 17:30:58.204272",
            updated_at="2025-02-08 17:30:58.204272"
        ),
        Group(
            id=2,
            group_icon=None,
            group_name="Group2",
            description="Another test group",
            created_at="2025-02-11 21:25:07.995633",
            updated_at="2025-02-11 21:25:07.995633"
        )
    ]
    db.session.add_all(groups)

    # Seed Event
    events = [
        Event(
            id=3,
            event_icon=None,
            description="Annual Hackathon 3",
            event_type="Tech Meetup",
            cost_to_attend=None,
            created_at="2025-02-08 19:23:49.784053",
            updated_at="2025-02-08 19:23:49.784053",
            location="NYC Convention Center",
            date="2025-06-15 10:00:00",
            photos=None,
            visibility="Public",
            category=None,
            id_discussion_thread=None,
            group_id=1,
            event_name=None
        ),
        Event(
            id=2,
            event_icon=None,
            description="Updated Hackathon 2025",
            event_type="Technology",
            cost_to_attend="50",
            created_at="2025-02-08 19:11:58.38696",
            updated_at="2025-02-08 19:35:37.358691",
            location="San Francisco",
            date="2025-07-20 12:00:00",
            photos=None,
            visibility="Public",
            category="Category1",
            id_discussion_thread=None,
            group_id=1,
            event_name=None
        ),
        Event(
            id=4,
            event_icon=None,
            description="A visit to the capital of love (Actually not...)",
            event_type="City Break",
            cost_to_attend=None,
            created_at="2025-02-11 21:25:07.996637",
            updated_at="2025-02-11 21:25:07.996637",
            location="Eiffel Tower",
            date="2025-06-15 11:00:00",
            photos=None,
            visibility="Public",
            category=None,
            id_discussion_thread=None,
            group_id=2,
            event_name="Paris Tour"
        )
    ]
    db.session.add_all(events)

    # Seed Expense
    expenses = [
        Expense(
            id=1,
            description="Venue Rental",
            created_at="2025-02-08 20:45:01.299789",
            updated_at="2025-02-08 22:15:36.527711",
            amount=500,
            amount_paid=110,
            amount_remaining=390,
            currency="USD",
            event_id=2
        ),
        Expense(
            id=2,
            description="Paris city bus",
            created_at="2025-02-11 21:25:07.999605",
            updated_at="2025-02-11 21:25:07.999605",
            amount=200,
            amount_paid=0,
            amount_remaining=200,
            currency="USD",
            event_id=4
        ),
        Expense(
            id=3,
            description="Baguette (an expensive one)",
            created_at="2025-02-11 21:25:07.999605",
            updated_at="2025-02-11 21:25:07.999605",
            amount=25,
            amount_paid=0,
            amount_remaining=25,
            currency="USD",
            event_id=4
        ),
        Expense(
            id=4,
            description="Rental",
            created_at="2025-02-11 21:25:07.999605",
            updated_at="2025-02-11 21:25:07.999605",
            amount=1200,
            amount_paid=0,
            amount_remaining=1200,
            currency="USD",
            event_id=4
        )
    ]
    db.session.add_all(expenses)

    # Seed ExpenseSplit
    expense_splits = [
        ExpenseSplit(id=1, user_id=3, algorithm_used="equally", amount_owed=166.67, amount_paid=0, expense_id=1),
        ExpenseSplit(id=2, user_id=4, algorithm_used="equally", amount_owed=56.67, amount_paid=110, expense_id=1),
        ExpenseSplit(id=3, user_id=5, algorithm_used="equally", amount_owed=166.67, amount_paid=0, expense_id=1),
        ExpenseSplit(id=4, user_id=3, algorithm_used="equally", amount_owed=130, amount_paid=0, expense_id=1),
        ExpenseSplit(id=5, user_id=4, algorithm_used="equally", amount_owed=130, amount_paid=0, expense_id=1),
        ExpenseSplit(id=6, user_id=5, algorithm_used="equally", amount_owed=130, amount_paid=0, expense_id=1),
        ExpenseSplit(id=7, user_id=5, algorithm_used="equally", amount_owed=195, amount_paid=0, expense_id=1),
        ExpenseSplit(id=8, user_id=6, algorithm_used="equally", amount_owed=195, amount_paid=0, expense_id=1),
        ExpenseSplit(id=9, user_id=5, algorithm_used="equally", amount_owed=12.5, amount_paid=0, expense_id=3),
        ExpenseSplit(id=10, user_id=6, algorithm_used="equally", amount_owed=12.5, amount_paid=0, expense_id=3),
        ExpenseSplit(id=11, user_id=5, algorithm_used="percentage", amount_owed=720, amount_paid=0, expense_id=4),
        ExpenseSplit(id=12, user_id=6, algorithm_used="percentage", amount_owed=480, amount_paid=0, expense_id=4),
        ExpenseSplit(id=13, user_id=5, algorithm_used="custom", amount_owed=157, amount_paid=0, expense_id=2),
        ExpenseSplit(id=14, user_id=6, algorithm_used="custom", amount_owed=43, amount_paid=0, expense_id=2)
    ]
    db.session.add_all(expense_splits)

    # Commit Users and Group tables to make sure they exist in the database
    db.session.commit()

    # Seed user_group many to many relationship table
    insert_data = [
        {'user_id': 3, 'group_id': 1}, 
        {'user_id': 4, 'group_id': 1}, 
        {'user_id': 5, 'group_id': 1},
        {'user_id': 6, 'group_id': 1},
        {'user_id': 7, 'group_id': 2},
        {'user_id': 6, 'group_id': 2},
        {'user_id': 5, 'group_id': 2},
    ]
    for row in insert_data:
        db.session.execute(user_group.insert().values(row))

    # Commit the user-group relationship insertion
    db.session.commit()

    print("Database seeding complete")