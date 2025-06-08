from peewee import Model, SqliteDatabase, CharField, IntegerField, IdentityField, ForeignKeyField
import peewee

# Initialize the database
sqldb = SqliteDatabase('scorekeeper.sqldb')

class BaseModel(Model):
    class Meta:
        database = sqldb

class Gang(BaseModel):
    id = IdentityField(primary_key=True, auto_increment=True)
    name = CharField(unique=True)
    
class Duel(BaseModel):
    id = IdentityField(primary_key=True, auto_increment=True)
    attacking_gang = ForeignKeyField(Gang, backref='duels_as_attacker')
    defending_gang = ForeignKeyField(Gang, backref='duels_as_defender')
    attacking_score = IntegerField(default=0)
    defending_score = IntegerField(default=0)

class ScorekeeperDB:
    def __init__(self):
        self.gang = self.GangOps()
        self.duel = self.DuelOps()

    def initialize_db(self):
        """Initialize the database and create tables if they do not exist."""
        sqldb.connect()
        sqldb.create_tables([Gang, Duel], safe=True)  # type: ignore
        sqldb.close()

    def close_db(self):
        """Close the database connection."""
        if not sqldb.is_closed():
            sqldb.close()
            print("Database connection closed.")
        else:
            print("Database connection is already closed.")

    class GangOps:
        def create(self, name: str) -> Gang:
            """Create a new gang with the given name."""
            if name.strip() == "":
                raise ValueError("Gang name cannot be empty.")
            if Gang.select().where(Gang.name == name).exists():  # type: ignore
                raise ValueError(f"A gang with the name '{name}' already exists.")
            return Gang.create(name=name)  # type: ignore

        def delete(self, gang: Gang) -> None:
            """Delete a gang from the database."""
            gang.delete_instance()  # type: ignore
            print(f"Gang '{gang.name}' deleted successfully.")  # type: ignore

        def get_by_id(self, gang_id: int) -> Gang:
            """Retrieve a gang by its ID."""
            try:
                return Gang.get(Gang.id == gang_id)  # type: ignore
            except peewee.DoesNotExist:
                raise ValueError(f"No gang found with ID {gang_id}.")

        def get_by_name(self, name: str) -> Gang:
            """Retrieve a gang by its name."""
            try:
                return Gang.get(Gang.name == name)  # type: ignore
            except peewee.DoesNotExist:
                raise ValueError(f"No gang found with the name '{name}'.")

        def get_all(self) -> list[Gang]:
            """Retrieve all gangs."""
            return list(Gang.select())  # type: ignore

        def update_name(self, gang: Gang, new_name: str) -> Gang:
            """Update the name of a gang."""
            if new_name.strip() == "":
                raise ValueError("Gang name cannot be empty.")
            if Gang.select().where(Gang.name == new_name).exists():  # type: ignore
                raise ValueError(f"A gang with the name '{new_name}' already exists.")
            gang.name = new_name  # type: ignore
            gang.save()  # type: ignore
            return gang  # type: ignore

    class DuelOps:
        def create(self, attacking_gang: Gang, defending_gang: Gang) -> Duel:
            """Create a new duel between two gangs."""
            if attacking_gang == defending_gang:
                raise ValueError("A gang cannot duel itself.")
            return Duel.create(attacking_gang=attacking_gang, defending_gang=defending_gang)  # type: ignore

        def delete(self, duel: Duel) -> None:
            """Delete a duel from the database."""
            duel.delete_instance()  # type: ignore
            print(f"Duel between '{duel.attacking_gang.name}' and '{duel.defending_gang.name}' deleted successfully.")  # type: ignore

        def get_by_id(self, duel_id: int) -> Duel:
            """Retrieve a duel by its ID."""
            try:
                return Duel.get(Duel.id == duel_id)  # type: ignore
            except peewee.DoesNotExist:
                raise ValueError(f"No duel found with ID {duel_id}.")

        def get_by_gang(self, gang: Gang) -> list[Duel]:
            """Retrieve all duels involving a specific gang."""
            duels_as_attacker = Duel.select().where(Duel.attacking_gang == gang)  # type: ignore
            duels_as_defender = Duel.select().where(Duel.defending_gang == gang)  # type: ignore
            return list(duels_as_attacker) + list(duels_as_defender)  # type: ignore

        def get_all(self) -> list[Duel]:
            """Retrieve all duels."""
            return list(Duel.select())  # type: ignore

        def get_recent(self, limit: int = 6) -> list[Duel]:
            """Retrieve the most recent duels."""
            return list(Duel.select().order_by(Duel.id.desc()).limit(limit))  # type: ignore

        def update_scores(self, duel: Duel, attacking_score: int, defending_score: int) -> Duel:
            """Update the scores of a duel."""
            if attacking_score < 0 or defending_score < 0:
                raise ValueError("Scores cannot be negative.")
            duel.attacking_score = attacking_score  # type: ignore
            duel.defending_score = defending_score  # type: ignore
            duel.save()  # type: ignore
            return duel  # type: ignore

