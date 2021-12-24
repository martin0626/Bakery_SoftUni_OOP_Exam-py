from project.baked_food.bread import Bread
from project.baked_food.cake import Cake
from project.drink.water import Water
from project.drink.tea import Tea
from project.table.inside_table import InsideTable
from project.table.outside_table import OutsideTable


class Bakery:

    def __init__(self, name):
        self.name = name
        self.food_menu = []
        self.drinks_menu = []
        self.tables_repository = []
        self.total_income = 0

    def add_food(self, food_type, name, price):
        food_instance = None

        if food_type == 'Bread':
            food_instance = Bread(name, price)

        elif food_type == 'Cake':
            food_instance = Cake(name, price)

        if food_instance:
            # TODO Possible mistake!!!
            if food_instance.name in [food.name for food in self.food_menu]:
                raise Exception(f'{food_type} {name} is already in the menu!')
            self.food_menu.append(food_instance)
            return f'Added {food_instance.name} ({food_type}) to the food menu'

    def add_drink(self, drink_type, name, portion, brand):
        drink_instance = None

        if drink_type == 'Tea':
            drink_instance = Tea(name, portion, brand)

        elif drink_type == 'Water':
            drink_instance = Water(name, portion, brand)

        if drink_instance:
            if drink_instance.name in [d.name for d in self.drinks_menu]:
                raise Exception(f'{drink_type} {name} is already in the menu!')
            self.drinks_menu.append(drink_instance)
            return f"Added {drink_instance.name} ({brand}) to the drink menu"

    def add_table(self, table_type, table_number, capacity):
        table_instance = None

        if table_type == 'InsideTable':
            table_instance = InsideTable(table_number, capacity)

        elif table_type == 'OutsideTable':
            table_instance = OutsideTable(table_number, capacity)

        if table_instance:
            if table_instance.table_number in [t.table_number for t in self.tables_repository]:
                raise Exception(f'Table {table_number} is already in the bakery!')
            self.tables_repository.append(table_instance)
            return f'Added table number {table_number} in the bakery'

    def reserve_table (self, number_of_people):
        for table in self.tables_repository:
            if not table.is_reserved and table.capacity >= number_of_people:
                table.reserve(number_of_people)
                return f"Table {table.table_number} has been reserved for {number_of_people} people"
        return f"No available table for {number_of_people} people"

    def order_food(self, table_number, *food_names):
        all_table_numbers = [t.table_number for t in self.tables_repository]
        all_food_names = {f.name: f for f in self.food_menu}

        if table_number not in all_table_numbers:
            return f"Could not find table {table_number}"

        table = [t for t in self.tables_repository if t.table_number == table_number][0]
        result = [f'Table {table_number} ordered:']
        not_in_menu_foods = []

        for food_name in food_names:
            if food_name in all_food_names:
                food = all_food_names[food_name]
                table.order_food(food)
                result.append(food.__repr__())
            else:
                not_in_menu_foods.append(food_name)
        string_foods_not_in_menu = '\n'.join(not_in_menu_foods)
        result.append(f'{self.name} does not have in the menu:\n{string_foods_not_in_menu}')
        return '\n'.join(result)

    def order_drink(self, table_number, *drinks_names):
        all_table_numbers = [t.table_number for t in self.tables_repository]
        all_drinks = {d.name: d for d in self.drinks_menu}
        if table_number not in all_table_numbers:
            return f"Could not find table {table_number}"

        result = [f'Table {table_number} ordered:']
        not_in_menu_drinks = []
        table = [t for t in self.tables_repository if t.table_number == table_number][0]

        for drink_name in drinks_names:
            if drink_name in all_drinks:
                drink = all_drinks[drink_name]
                table.order_drink(drink)
                result.append(drink.__repr__())
            else:
                not_in_menu_drinks.append(drink_name)
        string_drinks_not_in_menu = '\n'.join(not_in_menu_drinks)
        result.append(f'{self.name} does not have in the menu:\n{string_drinks_not_in_menu}')
        return "\n".join(result)

    def leave_table(self, table_number):
        table = [t for t in self.tables_repository if t.table_number == table_number][0]
        result = f'Table: {table_number}\nBill: {table.get_bill():.2f}'
        self.total_income += table.get_bill()
        table.clear()
        return result

    def get_free_tables_info(self):
        result = []
        for table in self.tables_repository:
            text = table.free_table_info()
            if text:
                result.append(text)
        if result:
            return '\n'.join(result)

    def get_total_income(self):
        for table in self.tables_repository:
            self.total_income += table.get_bill()

        return f"Total income: {self.total_income:.2f}lv"
