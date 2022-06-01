import logging
from flask import Flask, send_from_directory
from main.show_foto import show_foto_blueprint
from loader.load_foto import load_foto_blueprint
import  loggers


app = Flask(__name__)

app.register_blueprint(show_foto_blueprint)
app.register_blueprint(load_foto_blueprint)

app.config['POST_PATH'] = 'data/posts.json'
app.config['UPLOAD_FOLDER'] = 'uploads/images'

loggers.create_logger()

logger = logging.getLogger("basic")

# @app.route("/")
# def page_index():
#     pass
#
#
# @app.route("/list")
# def page_tag():
#     pass
#
#
# @app.route("/post", methods=["GET", "POST"])
# def page_post_form():
#     pass
#
#
# @app.route("/post", methods=["POST"])
# def page_post_upload():
#     pass
#
#
@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)


logger.info("Приложение запущено")

if __name__ == '__main__':
    app.run(debug=True)

