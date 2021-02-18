@app.route('/', methods=['GET'])
def get():
    return jsonify({'message': 'Hello world'})
