#!flask/bin/python
from app import app

app.run(host='0.0.0.0', port=8241, debug=False)
#ssl_context=('cert.pem', 'key.pem'),
