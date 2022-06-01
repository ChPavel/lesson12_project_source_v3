import os.path
import random

from flask import Blueprint, request, render_template, current_app

import templates as templates
from classes.data_manager import DataManager
from .exceptions import OutOfFreeNamesError, PictureFormatNotSupportedError, PictureNotUplosderError
from .upload_manager import UploadManager


load_foto_blueprint = Blueprint('load_foto_blueprint', __name__, template_folder=templates)



@load_foto_blueprint.route('/post', methods=['GET'])
def page_form():
    return render_template('post_form.html')


@load_foto_blueprint.route('/post', methods=['POST'])
def page_create_posts():

    path = current_app.config.get('POST_PATH')
    data_manager = DataManager(path)
    upload_manager = UploadManager()

    # Получаем данные.
    picture = request.files.get('picture', None)
    content = request.values.get('content', '')

    # Сохраняем картинку с помощью менеджера загрузок.
    filename_saved = upload_manager.save_with_random_name(picture)

    # Получаем путь для браузера клиента.
    web_path = f"/uploads/images/{filename_saved}"

    # Создаём данные для записи в файл.
    post = {"pic":web_path, "content": content}

    # Добавляем данные в файл.
    data_manager.add(post)

    return render_template("post_uploaded.html", pic=web_path, content=content)

@load_foto_blueprint.errorhandler(OutOfFreeNamesError)
def error_out_of_free_names(e):
    return  "Закончились свободные имена для загрузки картинок. Обратитесь к администратору сайта."


@load_foto_blueprint.errorhandler(PictureFormatNotSupportedError)
def error_picture_format_not_supported(e):
    return  "Формат картинки не поддерживается, выберите другой."


@load_foto_blueprint.errorhandler(PictureNotUplosderError)
def error_picture_not_uplosder(e):
    return  "Не удалось загрузить картинку."