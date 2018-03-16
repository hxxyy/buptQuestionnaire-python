from flask import Flask
from flask_graphql import GraphQLView
from schema import schema
from flask_cors import CORS
import os
import socket
import qrcode

app = Flask(__name__, static_folder=os.path.join(os.path.curdir, 'pwa-mat'), static_url_path='')
app.debug = True

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
app.add_url_rule('/api/graphql', view_func=GraphQLView.as_view('graphql1', schema=schema, graphiql=True))
CORS(app)


@app.route('/')
def index():
    return app.send_static_file("index.html")


if __name__ == '__main__':
    # host = socket.gethostbyname(socket.gethostname()) + ':8081'
    # img = qrcode.make(host)
    # img.save('host.png')
    # os.system('open %s' % os.path.join(os.path.dirname(__file__), 'host.png'))
    # print('Your app is running on [%s]' % host)
    app.run(host='0.0.0.0', port=8081)
