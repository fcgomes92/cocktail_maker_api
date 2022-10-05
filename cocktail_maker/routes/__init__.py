from functools import wraps

from cocktail_maker.db import db, models
from cocktail_maker.routes.utils import (create_instance, dump_route,
                                         get_instances, validate_schema)
from cocktail_maker.schemas import (BaseSchema, IngredientsSchema,
                                    RecipeCreateSchema, RecipeSchema,
                                    TagsSchema)
from cocktail_maker.services.recipes import RecipeService
from sqlalchemy import select


def load_routes(app, config):
    @app.route('/tags', methods=['POST'])
    @validate_schema(TagsSchema)
    @create_instance(models.Tag)
    def post_tags(*args, **kwargs):
        return dump_route(TagsSchema, kwargs.get('model_instance'))
    
    @app.route('/tags/<id>', methods=['POST'])
    @validate_schema(TagsSchema)
    @get_instances(models.Tag, many=False)
    def post_tags_id(*args, **kwargs):
        model = kwargs.get('model_instance')
        data = kwargs.get('schema_data', {})
        model.name = data.get('name')
        db.session().commit()
        return dump_route(IngredientsSchema, model)

    @app.route('/tags', methods=['GET'])
    @get_instances(models.Tag)
    def get_tags(*args, **kwargs):
        return dump_route(TagsSchema, kwargs.get('model_instance'), many=True)

    @app.route('/ingredients', methods=['GET'])
    @get_instances(models.Ingredient)
    def get_ingredients(*args, **kwargs):
        return dump_route(IngredientsSchema, kwargs.get('model_instance'), many=True)

    @app.route('/ingredients/<id>', methods=['GET'])
    @get_instances(models.Ingredient, many=False)
    def get_ingredient(*args, **kwargs):
        return dump_route(IngredientsSchema, kwargs.get('model_instance'), many=False)

    @app.route('/ingredients', methods=['POST'])
    @validate_schema(IngredientsSchema)
    @create_instance(models.Ingredient)
    def post_ingredients(*args, **kwargs):
        return dump_route(IngredientsSchema, kwargs.get('model_instance'))
    
    @app.route('/ingredients/<id>', methods=['POST'])
    @validate_schema(IngredientsSchema)
    @get_instances(models.Ingredient, many=False)
    def post_ingredients_id(*args, **kwargs):
        model = kwargs.get('model_instance')
        data = kwargs.get('schema_data', {})
        model.name = data.get('name')
        model.description = data.get('description')
        model.density = data.get('density')
        db.session().commit()
        return dump_route(IngredientsSchema, model)

    @app.route('/recipes', methods=['GET'])
    @get_instances(models.Recipe)
    def get_recipes(*args, **kwargs):
        return dump_route(RecipeSchema, kwargs.get('model_instance'), many=True)

    @app.route('/recipes/<id>', methods=['GET'])
    @get_instances(models.Recipe, many=False)
    def get_recipe(*args, **kwargs):
        return dump_route(RecipeSchema, kwargs.get('model_instance'), many=False)

    @app.route('/recipes', methods=['POST'])
    @validate_schema(RecipeCreateSchema)
    def post_recipes(*args, **kwargs):
        scheme_data = kwargs.get('schema_data', {})
        recipe = RecipeService.create_recipe(scheme_data)
        return dump_route(RecipeSchema, recipe)

    @app.route('/recipes/<id>', methods=['POST'])
    @validate_schema(RecipeCreateSchema)
    def post_recipes_id(*args, **kwargs):
        scheme_data = kwargs.get('schema_data', {})
        recipe = RecipeService.update_recipe(scheme_data, kwargs.get('id'))
        return dump_route(RecipeSchema, recipe)
