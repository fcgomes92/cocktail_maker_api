from cocktail_maker.db import db
from cocktail_maker.db.models import Ingredient, Recipe, RecipeIngredient, Tag
from sqlalchemy import select


class RecipeService():
    @classmethod
    def handle_ingredient_list(cls, recipe: Recipe, ingredients):
        ingredients_ids = set(map(lambda i: i.get('ingredient_id'), ingredients))
        current_ingredients = set(map(lambda i: i.ingredient_id, recipe.ingredients))
        
        new_ingredients_ids = list(ingredients_ids - current_ingredients)
        deleted_ids = list(current_ingredients - ingredients_ids)
        
        existing_ingredients = recipe.ingredients
        new_ingredients = [RecipeIngredient(recipe_id=recipe.id, **ingredient) for ingredient in ingredients if ingredient.get('ingredient_id') in new_ingredients_ids]
        all_ingredients = [*existing_ingredients, *new_ingredients]
        
        return [i for i in all_ingredients if i.ingredient_id in ingredients_ids]

    @classmethod
    def handle_tags_list(cls, tags):
        return list(map(lambda i: db.session.execute(
            select(Tag).where(Tag.id == i)).fetchone()[0], tags))

    @classmethod
    def handle_data_format(cls, data: dict):
        ingredients = data.get('ingredients', [])
        tags = data.get('tags', [])
        raw_data = {**data}
        del raw_data['ingredients']
        del raw_data['tags']
        return [ingredients, tags, raw_data]

    @classmethod
    def update_recipe(cls, data: dict, id: int):
        ingredients, tags, raw_data = cls.handle_data_format(data)
        recipe = Recipe.find_one(id)
        
        recipe.ingredients = cls.handle_ingredient_list(
            recipe=recipe, ingredients=ingredients)
        recipe.tags = cls.handle_tags_list(tags=tags)
        recipe.name = raw_data['name']
        recipe.description =raw_data['description']
        recipe.rate =raw_data['rate']

        # db.session.add(recipe)
        db.session.commit()
        
        return recipe
        
    @classmethod
    def create_recipe(cls, data: dict):
        ingredients, tags, raw_data = cls.handle_data_format(data)
        recipe = Recipe(**raw_data)

        recipe.ingredients = cls.handle_ingredient_list(
            recipe=recipe, ingredients=ingredients)
        recipe.tags = cls.handle_tags_list(tags=tags)

        db.session.add(recipe)
        db.session.commit()

        return recipe
