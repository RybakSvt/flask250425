from flask import Blueprint, request, jsonify
from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from src.dtos.questions import PollCreateRequest, PollResponse, PollUpdateRequest
from src.dtos.questions import PollOptionCreateRequest
from src.models import Poll, PollOption, Category
from src.core.db import db

questions_bp = Blueprint("questions", __name__, url_prefix='/questions')


# R - Get All Questions (Polls)
@questions_bp.route('', methods=["GET"])
def list_of_questions() -> Any:
    try:
        stmt = select(Poll).options(
            selectinload(Poll.category),
            selectinload(Poll.options)
        )
        polls = db.session.scalars(stmt).all()

        polls_response = []
        for poll in polls:
            poll_dict = {
                **poll.to_dict(),
                'category': poll.category.to_dict() if poll.category else None,
                'options': [option.to_dict() for option in poll.options]
            }
            polls_response.append(PollResponse.model_validate(poll_dict).model_dump())

        return jsonify(polls_response), 200

    except Exception as exc:
        return jsonify({
            "error": "Unexpected Error",
            "message": str(exc)
        }), 500


# C - Create Question (Poll)
@questions_bp.route('/create', methods=["POST"])
def create_new_question():
    try:
        raw_data: dict[str, Any] = request.get_json()

        if not raw_data:
            return jsonify({
                "error": "Validation Error",
                "message": "Сырых данных не обнаружено"
            }), 400

        poll_data = PollCreateRequest.model_validate(raw_data)

        # Проверяем существование категории
        category_stmt = select(Category).where(Category.id == poll_data.category_id)
        category = db.session.scalar(category_stmt)

        if not category:
            return jsonify({
                "error": "Validation Error",
                "message": f"Категория с ID {poll_data.category_id} не найдена"
            }), 400

        options_data = poll_data.options
        poll_dict: dict[str, Any] = poll_data.model_dump(exclude={'options'})

        poll: Poll = Poll(**poll_dict)

        db.session.add(poll)
        db.session.flush()

        for opt in options_data:  # type: PollOptionCreateRequest
            option: PollOption = PollOption(
                poll_id=poll.id,
                text=opt.text
            )
            poll.options.append(option)

        db.session.commit()
        db.session.refresh(poll)

        # Загружаем полные данные для ответа
        poll_stmt = select(Poll).options(
            selectinload(Poll.category),
            selectinload(Poll.options)
        ).where(Poll.id == poll.id)

        poll_with_relations = db.session.scalar(poll_stmt)

        # poll_response: dict[str, Any] = (
        #     PollResponse
        #     .model_validate(poll_with_relations)
        #     .model_dump()
        # )

        # Преобразуем категорию в словарь для сериализации
        poll_dict = {
            **poll_with_relations.to_dict(),
            'category': poll_with_relations.category.to_dict() if poll_with_relations.category else None,
            'options': [option.to_dict() for option in poll_with_relations.options]
        }

        poll_response: dict[str, Any] = (
            PollResponse
            .model_validate(poll_dict)  # ← Передаем словарь
            .model_dump()
        )

        return jsonify(poll_response), 201

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


# R - Get Question by ID
@questions_bp.route('/<int:question_id>', methods=["GET"])
def get_question_by_id(question_id: int) -> Any:
    try:
        stmt = select(Poll).options(
            selectinload(Poll.category),
            selectinload(Poll.options)
        ).where(Poll.id == question_id)

        poll = db.session.scalar(stmt)

        if not poll:
            return jsonify({
                "error": "Not Found",
                "message": f"Опрос с ID {question_id} не найден"
            }), 404

        poll_dict = {
            **poll.to_dict(),
            'category': poll.category.to_dict() if poll.category else None,
            'options': [option.to_dict() for option in poll.options]
        }

        poll_response = PollResponse.model_validate(poll_dict).model_dump()

        return jsonify(poll_response), 200

    except Exception as exc:
        return jsonify({
            "error": "Unexpected Error",
            "message": str(exc)
        }), 500


# U - Update Question
@questions_bp.route('/<int:question_id>/update', methods=["PUT", "PATCH"])
def update_question(question_id: int) -> Any:
    try:
        raw_data: dict[str, Any] = request.get_json()

        if not raw_data:
            return jsonify({
                "error": "Validation Error",
                "message": "Данные не предоставлены"
            }), 400

        stmt = select(Poll).where(Poll.id == question_id)
        poll = db.session.scalar(stmt)

        if not poll:
            return jsonify({
                "error": "Not Found",
                "message": f"Опрос с ID {question_id} не найден"
            }), 404

        update_data = PollUpdateRequest.model_validate(raw_data)

        # Проверяем категорию, если она обновляется
        if update_data.category_id is not None:
            category_stmt = select(Category).where(Category.id == update_data.category_id)
            category = db.session.scalar(category_stmt)

            if not category:
                return jsonify({
                    "error": "Validation Error",
                    "message": f"Категория с ID {update_data.category_id} не найдена"
                }), 400
            poll.category_id = update_data.category_id

        # Обновляем остальные поля
        if update_data.title is not None:
            poll.title = update_data.title
        if update_data.description is not None:
            poll.description = update_data.description
        if update_data.start_date is not None:
            poll.start_date = update_data.start_date
        if update_data.end_date is not None:
            poll.end_date = update_data.end_date
        if update_data.is_active is not None:
            poll.is_active = update_data.is_active
        if update_data.is_anonymous is not None:
            poll.is_anonymous = update_data.is_anonymous

        db.session.commit()
        db.session.refresh(poll)

        # Загружаем обновленные данные с отношениями
        updated_stmt = select(Poll).options(
            selectinload(Poll.category),
            selectinload(Poll.options)
        ).where(Poll.id == question_id)

        updated_poll = db.session.scalar(updated_stmt)

        # Преобразуем в словарь для сериализации
        poll_dict = {
            **updated_poll.to_dict(),
            'category': updated_poll.category.to_dict() if updated_poll.category else None,
            'options': [option.to_dict() for option in updated_poll.options]
        }

        poll_response = PollResponse.model_validate(poll_dict).model_dump()

        return jsonify(poll_response), 200

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


# D - Delete Question
@questions_bp.route('/<int:question_id>/delete', methods=["DELETE"])
def delete_question(question_id: int) -> Any:
    try:
        stmt = select(Poll).where(Poll.id == question_id)
        poll = db.session.scalar(stmt)

        if not poll:
            return jsonify({
                "error": "Not Found",
                "message": f"Опрос с ID {question_id} не найден"
            }), 404

        db.session.delete(poll)
        db.session.commit()

        return jsonify({
            "message": f"Опрос с ID {question_id} успешно удален"
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