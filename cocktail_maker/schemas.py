from marshmallow import Schema, fields


class BaseSchema(Schema):
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class TagsSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class BaseRecipeSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    description = fields.String()
    author = fields.String()
    rate = fields.String(default=0)
    tags = fields.Nested(TagsSchema, dump_only=True, many=True)


class IngredientRecipeSchema(BaseSchema):
    recipe = fields.Nested(BaseRecipeSchema)
    amount = fields.Float()
    unit = fields.String()


class IngredientsBaseSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    description = fields.String()
    density = fields.Float()
    amount = fields.Float()
    unit = fields.String()


class IngredientsSchema(IngredientsBaseSchema):
    recipes = fields.Nested(IngredientRecipeSchema, many=True, dump_only=True)


class RecipeIngredientCreateSchema(BaseSchema):
    ingredient_id = fields.Integer()
    amount = fields.Float()
    unit = fields.String()


class RecipeCreateSchema(BaseRecipeSchema):
    ingredients = fields.List(fields.Nested(
        RecipeIngredientCreateSchema), default=[])
    tags = fields.List(fields.Integer, default=[])


class RecipeIngredientSchema(BaseSchema):
    ingredient = fields.Nested(IngredientsBaseSchema)
    amount = fields.Float()
    unit = fields.String()


class RecipeSchema(BaseRecipeSchema):
    ingredients = fields.Nested(
        RecipeIngredientSchema, dump_only=True, many=True)
