import peewee as pw

db = pw.SqliteDatabase("chess.db")


class BaseModel(pw.Model):
    class Meta:
        database = db


class Piece(BaseModel):
    name = pw.CharField(primary_key=True)
    icon = pw.CharField()

    class Meta:
        table_name = "piece"

    def add_default_pieces():
        Piece.insert_many(
            [
                {"name": "Queen", "icon": "Q"},
                {"name": "King", "icon": "K"},
                {"name": "Bishop", "icon": "B"},
                {"name": "Knight", "icon": "N"},
                {"name": "Rook", "icon": "R"},
                {"name": "Pawn", "icon": "P"},
            ]
        ).execute(db)

    def init_data():
        if not Piece.table_exists():
            Piece.create_table()

        if len(Piece.select()) == 0:
            Piece.add_default_pieces()
