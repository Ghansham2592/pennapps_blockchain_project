# from flask import Flask, render_template
# app = Flask(__name__, template_folder='new_html')


# @app.route('/alpha')
# def alpha():
#     return "This is the alpha version"

# @app.route('/beta')
# def beta():
#     return "This is the beta version"

 
# # @app.route('/')
# # def display():
# #     return "Looks like it works!"


# @app.route('/')
# def render():
#     return render_template('index.html')

# if __name__=='__main__':
#     app.run(debug=True)



from flask import Flask

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path="/new_html", static_folder='/media/harshad/work/pennapps/new_html')

@app.route('/')
def static_file():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run()