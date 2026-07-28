import random

from django.core.management.base import BaseCommand
from faker import Faker

from kitchen.models import Cook, Dish, DishType

fake = Faker()

DISH_TYPES = [
    "Appetizer",
    "Main Course",
    "Dessert",
    "Soup",
    "Salad",
    "Side Dish",
    "Beverage",
    "Breakfast",
    "Snack",
    "Seafood",
]

DISH_NAMES = {
    "Appetizer": [
        "Bruschetta", "Spring Rolls", "Garlic Bread",
        "Stuffed Mushrooms", "Mozzarella Sticks",
    ],
    "Main Course": [
        "Grilled Salmon", "Beef Stroganoff", "Chicken Parmesan",
        "Lamb Chops", "Pork Tenderloin",
    ],
    "Dessert": [
        "Tiramisu", "Cheesecake", "Chocolate Mousse",
        "Panna Cotta", "Apple Pie",
    ],
    "Soup": [
        "Tomato Soup", "French Onion Soup", "Minestrone",
        "Clam Chowder", "Borscht",
    ],
    "Salad": [
        "Caesar Salad", "Greek Salad", "Waldorf Salad",
        "Caprese Salad", "Cobb Salad",
    ],
    "Side Dish": [
        "Mashed Potatoes", "Grilled Vegetables",
        "Rice Pilaf", "Coleslaw", "French Fries",
    ],
    "Beverage": [
        "Fresh Lemonade", "Iced Tea", "Smoothie",
        "Hot Chocolate", "Fresh Orange Juice",
    ],
    "Breakfast": [
        "Pancakes", "Eggs Benedict", "French Toast",
        "Omelette", "Granola Bowl",
    ],
    "Snack": [
        "Nachos", "Hummus Plate", "Cheese Platter",
        "Popcorn Shrimp", "Chicken Wings",
    ],
    "Seafood": [
        "Lobster Bisque", "Shrimp Scampi", "Fish Tacos",
        "Crab Cakes", "Grilled Octopus",
    ],
}


class Command(BaseCommand):
    help = "Seed the database with sample data using Faker"  # noqa: VNE003

    def add_arguments(self, parser):
        parser.add_argument(
            "--cooks",
            type=int,
            default=10,
            help="Number of cooks to create (default: 10)",
        )
        parser.add_argument(
            "--dishes",
            type=int,
            default=30,
            help="Number of dishes to create (default: 30)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding",
        )

    def handle(self, *args, **options):
        num_cooks = options["cooks"]
        num_dishes = options["dishes"]

        if options["clear"]:
            self.stdout.write("Clearing existing data...")
            Dish.objects.all().delete()
            DishType.objects.all().delete()
            Cook.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS("Data cleared."))

        dish_types = self._create_dish_types()
        cooks = self._create_cooks(num_cooks)
        self._create_dishes(num_dishes, dish_types, cooks)

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded: "
            f"{len(dish_types)} dish types, "
            f"{len(cooks)} cooks, "
            f"{num_dishes} dishes"
        ))

    def _create_dish_types(self):
        dish_types = []
        for name in DISH_TYPES:
            dish_type, created = DishType.objects.get_or_create(
                name=name
            )
            dish_types.append(dish_type)
            if created:
                self.stdout.write(
                    f"  Created dish type: {name}"
                )
        return dish_types

    def _create_cooks(self, count):
        cooks = []
        for _ in range(count):
            username = fake.unique.user_name()
            cook = Cook.objects.create_user(
                username=username,
                password="testpass123",
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                years_of_experience=random.randint(0, 30),
            )
            cooks.append(cook)
            self.stdout.write(
                f"  Created cook: {cook.username} "
                f"({cook.years_of_experience} yrs exp)"
            )
        return cooks

    def _create_dishes(self, count, dish_types, cooks):
        all_cooks = list(Cook.objects.all())
        for i in range(count):
            dish_type = random.choice(dish_types)
            names = DISH_NAMES.get(dish_type.name, [])

            if names and i < len(DISH_TYPES) * 5:
                idx = i % len(names)
                name = names[idx]
                if Dish.objects.filter(name=name).exists():
                    name = f"{name} {fake.word().capitalize()}"
            else:
                name = (
                    f"{fake.word().capitalize()} "
                    f"{fake.word().capitalize()}"
                )

            dish = Dish.objects.create(
                name=name,
                description=fake.paragraph(nb_sentences=3),
                price=round(random.uniform(3.99, 45.99), 2),
                dish_type=dish_type,
            )
            num_cooks = random.randint(1, min(3, len(all_cooks)))
            assigned = random.sample(all_cooks, num_cooks)
            dish.cooks.set(assigned)

            self.stdout.write(
                f"  Created dish: {dish.name} "
                f"({dish_type.name}) - ${dish.price}"
            )
