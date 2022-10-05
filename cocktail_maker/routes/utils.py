from functools import wraps

from cocktail_maker.db import db, models
from flask import request
from sqlalchemy import select


def validate_schema(ValidationSchema):
    def decorator(f):
        @wraps(f)
        def vfunc(*args, **kwargs):
            schema = ValidationSchema()
            data = schema.loads(request.data)
            return f(*args, schema_data=data, **kwargs)
        return vfunc
    return decorator


def create_instance(CreationModel: models.Model):
    def decorator(f):
        @wraps(f)
        def vfunc(*args, **kwargs):
            raw_data = kwargs.get('schema_data')
            instance = CreationModel(**raw_data)
            db.session.add(instance)
            db.session.commit()
            return f(*args, model_instance=instance, **kwargs)
        return vfunc
    return decorator


def get_instances(CreationModel: models.Model, many=True):
    def decorator(f):
        @wraps(f)
        def vfunc(*args, **kwargs):
            if many:
                result = db.session.execute(select(CreationModel))
                model_instance = result.scalars().all()
            else:
                result = db.session.execute(select(CreationModel).where(
                    CreationModel.id == kwargs.get('id')))
                model_instance = result.fetchone()[0]
            return f(*args, model_instance=model_instance, **kwargs)
        return vfunc
    return decorator


def dump_route(Schema, model_instance, many=False):
    schema = Schema(many=many)
    return schema.dumps(model_instance)
