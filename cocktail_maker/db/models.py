from . import db
from sqlalchemy import select


class Model(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime)


class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredient'

    recipe_id    = db.Column(db.ForeignKey("recipes.id"), primary_key=True)
    ingredient_id = db.Column(db.ForeignKey("ingredients.id"), primary_key=True)
    amount = db.Column(db.Float)
    unit = db.Column(db.String(16))
    recipe = db.relationship('Recipe', back_populates="ingredients")
    ingredient = db.relationship('Ingredient', back_populates="recipes")


RecipeTag = db.Table(
    "recipe_tag",
    Model.metadata,
    db.Column("id_recipe", db.ForeignKey("recipes.id"), primary_key=True),
    db.Column("id_tag", db.ForeignKey("tags.id"), primary_key=True)
)


class Recipe(Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True,
                   index=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    author = db.Column(db.String)
    rate = db.Column(db.Float, default=-1)
    ingredients = db.relationship("RecipeIngredient", back_populates="recipe", cascade="save-update, merge, delete, delete-orphan")
    tags = db.relationship("Tag", secondary=RecipeTag, backref="recipes")
    
    @classmethod
    def find_one(cls, id: int):
        stm = db.session.execute(select(Recipe).filter_by(id=id))
        result = stm.fetchone()[0]
        return result


class Ingredient(Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    density = db.Column(db.Float)
    recipes = db.relationship("RecipeIngredient", back_populates="ingredient", cascade="save-update, merge, delete, delete-orphan")


class Tag(Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True,
                   index=True, autoincrement=True)
    name = db.Column(db.String, unique=True)
