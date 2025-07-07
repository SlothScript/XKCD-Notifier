# A testing endpoint so I don't have to wait for XKCD to release a comic to test notifications

from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for fake comics
comics = {}
next_comic_number = 1


@app.route('/<int:comic_number>/info.0.json', methods=['GET'])
def get_comic(comic_number):
    if comic_number in comics:
        return jsonify(comics[comic_number])
    else:
        return jsonify({'error': 'Comic not found'}), 404


@app.route('/info.0.json', methods=['GET'])
def get_latest_comic():
    if not comics:
        return jsonify({'error': 'No comics found'}), 404
    latest_comic_number = max(comics.keys())
    return jsonify(comics[latest_comic_number])


# Use for creating comic
"""
curl -X POST http://127.0.0.1:5001/create \
      -H "Content-Type: application/json" \
      -d '{}'
"""
@app.route('/create', methods=['POST'])
def create_comic():
    global next_comic_number
    data = request.get_json()
    data['num'] = next_comic_number
    data['img'] = data.get('img', 'https://example.com/comic.png')
    data['title'] = data.get('title', f'Fake Comic {next_comic_number}')
    data['alt'] = data.get('alt', f'Alt text for fake comic {next_comic_number}')
    comics[next_comic_number] = data
    next_comic_number += 1
    return jsonify({'message': 'Comic created successfully', 'comic_number': next_comic_number - 1}), 201


if __name__ == '__main__':
    app.run(debug=True, port=5001)
