#from flask import Flask
#import config
#from main.views import main
#from blog.views import blog

#app = Flask(__name__)
#app.config.from_object('config')
#app.secret_key = config.SECRET_KEY

#app.register_blueprint(main, url_prefix='')
#app.register_blueprint(blog, url_prefix='/blog')
from main import app

app.run(debug=True)
