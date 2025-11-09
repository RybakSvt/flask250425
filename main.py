from flask import Flask


app = Flask(__name__)

# @app.route('/')
# def home_page() -> str:
#     return "HELLO FROM OUR FIRST FLASK APP!!!"
#
# @app.route('/products')
# def get_list_of_products() -> str:
#     # ...
#     return "LIST OF PRODUCTS"
#
#
# @app.route('/user/<string:username>')
# def get_user_info(username: str) -> str:
#     return f"'{username}' USER INFO"
#
# @app.route('/<int:user_id>')
# def get_user_by_id(user_id: int) -> str:
#     return f"USER ID '{user_id}'"
#
# @app.route('/files/<path:file_path>')
# def get_file_by_path(file_path: str) -> str:
#     return f"File with path '{file_path}'"

# Есть небольшой набор данных. Написать маршрут, который
# возвращает имя по user_id из этого набора данных и
# User not found -- если ничего не найдено.
#
users = {1: "Alice", 2: "Bob", 3: "Charlie"}

@app.route('/user/<int:user_id>')
def show_user_profile_by_id(user_id):
    # name = users.get(user_id, "User not found")
    # return name
    # if user_id in users:
    #     return users[user_id]
    # else:
    #     return "User not found"

    return users[user_id] if user_id in users else "User not found"






if __name__ == '__main__':
    app.run(debug=True)
