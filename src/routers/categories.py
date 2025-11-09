from flask import Blueprint, request, jsonify
from typing import Any, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from src.dtos.category import CategoryCreate, CategoryUpdate, CategoryResponse
from src.models import Category
from src.core.db import db

categories_bp = Blueprint("categories", __name__, url_prefix='/categories')


# C - Create Category
@categories_bp.route('', methods=["POST"])
def create_category():
    try:
        raw_data: dict[str, Any] = request.get_json()

        if not raw_data:
            return jsonify({
                "error": "Validation Error",
                "message": "Данные не предоставлены"
            }), 400

        category_data = CategoryCreate.model_validate(raw_data)

        # Проверяем, существует ли категория с таким именем
        stmt = select(Category).where(Category.name == category_data.name)
        existing_category = db.session.scalar(stmt)

        if existing_category:
            return jsonify({
                "error": "Validation Error",
                "message": "Категория с таким названием уже существует"
            }), 400

        category = Category(name=category_data.name)

        db.session.add(category)
        db.session.commit()
        db.session.refresh(category)

        category_response = CategoryResponse.model_validate(category).model_dump()

        return jsonify(category_response), 201

    except ValidationError as exc:
        return jsonify({
            "error": "Validation Error",
            "message": exc.errors()
        }), 400
    except SQLAlchemyError as exc:
        db.session.rollback()
        return jsonify({
            "error": "DATABASE Error",
            "message": str(exc)
        }), 400
    except Exception as exc:
        return jsonify({
            "error": "Unexpected Error",
            "message": str(exc)
        }), 500


# R - Get All Categories
@categories_bp.route('', methods=["GET"])
def get_all_categories():
    try:
        stmt = select(Category)
        categories = db.session.scalars(stmt).all()

        categories_response = [
            CategoryResponse.model_validate(category).model_dump()
            for category in categories
        ]

        return jsonify(categories_response), 200

    except Exception as exc:
        return jsonify({
            "error": "Unexpected Error",
            "message": str(exc)
        }), 500


# R - Get Category by ID
@categories_bp.route('/<int:category_id>', methods=["GET"])
def get_category_by_id(category_id: int):
    try:
        stmt = select(Category).where(Category.id == category_id)
        category = db.session.scalar(stmt)

        if not category:
            return jsonify({
                "error": "Not Found",
                "message": f"Категория с ID {category_id} не найдена"
            }), 404

        category_response = CategoryResponse.model_validate(category).model_dump()

        return jsonify(category_response), 200

    except Exception as exc:
        return jsonify({
            "error": "Unexpected Error",
            "message": str(exc)
        }), 500


# U - Update Category
@categories_bp.route('/<int:category_id>', methods=["PUT"])
def update_category(category_id: int):
    try:
        raw_data: dict[str, Any] = request.get_json()

        if not raw_data:
            return jsonify({
                "error": "Validation Error",
                "message": "Данные не предоставлены"
            }), 400

        stmt = select(Category).where(Category.id == category_id)
        category = db.session.scalar(stmt)

        if not category:
            return jsonify({
                "error": "Not Found",
                "message": f"Категория с ID {category_id} не найдена"
            }), 404

        update_data = CategoryUpdate.model_validate(raw_data)

        # Проверяем уникальность имени, если оно обновляется
        if update_data.name is not None:
            check_stmt = select(Category).where(
                Category.name == update_data.name,
                Category.id != category_id
            )
            existing_category = db.session.scalar(check_stmt)

            if existing_category:
                return jsonify({
                    "error": "Validation Error",
                    "message": "Категория с таким названием уже существует"
                }), 400

            category.name = update_data.name

        db.session.commit()
        db.session.refresh(category)

        category_response = CategoryResponse.model_validate(category).model_dump()

        return jsonify(category_response), 200

    except ValidationError as exc:
        return jsonify({
            "error": "Validation Error",
            "message": exc.errors()
        }), 400
    except SQLAlchemyError as exc:
        db.session.rollback()
        return jsonify({
            "error": "DATABASE Error",
            "message": str(exc)
        }), 400
    except Exception as exc:
        return jsonify({
            "error": "Unexpected Error",
            "message": str(exc)
        }), 500


# D - Delete Category
@categories_bp.route('/<int:category_id>', methods=["DELETE"])
def delete_category(category_id: int):
    try:
        stmt = select(Category).where(Category.id == category_id)
        category = db.session.scalar(stmt)

        if not category:
            return jsonify({
                "error": "Not Found",
                "message": f"Категория с ID {category_id} не найдена"
            }), 404

        # Проверяем, есть ли связанные опросы
        if category.polls:
            return jsonify({
                "error": "Conflict",
                "message": "Невозможно удалить категорию, так как с ней связаны опросы"
            }), 409

        db.session.delete(category)
        db.session.commit()

        return jsonify({
            "message": f"Категория с ID {category_id} успешно удалена"
        }), 200

    except SQLAlchemyError as exc:
        db.session.rollback()
        return jsonify({
            "error": "DATABASE Error",
            "message": str(exc)
        }), 400
    except Exception as exc:
        return jsonify({
            "error": "Unexpected Error",
            "message": str(exc)
        }), 500