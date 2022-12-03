from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Library(db.Model):
    """
    Class that represents a Library table.
    """
    __tablename__ = "library"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    open_hour = db.Column(db.Integer, nullable=False)
    close_hour = db.Column(db.Integer, nullable=False)
    map_image = db.Column(db.String, nullable=False)
    # location ?

    def __init__(self, **kwargs):
        """
        Creates a Library object.
        """
        self.name = kwargs.get("name", "")
        self.description = kwargs.get("description", "")
        self.open_hour = kwargs.get("open_hour", 8)
        self.close_hour = kwargs.get("close_hour", 20)
        self.map_image = kwargs.get("map_image", "")

    def serialize(self):
        """
        Serializes a Library object.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "open_hour": self.open_hour,
            "close_hour": self.close_hour,
            "map_image": self.map_image
        }

    def small_serialize(self):
        """
        Serializes a Library object for use in Favorite.
        """
        return {
            "name": self.name
        }


class Favorite(db.Model):
    """
    Class that represents a Favorite table.
    """
    __tablename__ = "favorite"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    building_id = db.Column(db.Integer, db.ForeignKey("library.id"))

    def __init__(self, **kwargs):
        """
        Creates a Favorite object.
        """
        pass

    def serialize(self):
        """
        Serializes a Favorite object.
        """
        library = Library.query.filter_by(id=self.building_id).first()
        return {
            "id": self.id,
            "building": library.small_serialize()
        }
