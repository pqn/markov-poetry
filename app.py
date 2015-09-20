from flask import Flask, render_template, request, url_for, jsonify
from poetry import markov_poem

app = Flask(__name__)
app.debug = True
@app.route('/')
def form():
    return render_template('form_submit.html')

@app.route('/poem', methods=['GET'])
def poem():
    txtName=request.args.get('txt')
    if txtName == '0':
        file = open("amendments.txt")
    elif txtName == '1':
        file = open("moby_dick.txt")
    elif txtName == '2':
        file = open("aesop.txt")
    elif txtName == '3':
        file = open("beatles.txt")
    elif txtName == '4':
        file = open("bible.txt")
    else:
        file = open("amendments.txt")
    txtName = file.read()
    txtName = markov_poem(txtName)
    return render_template('form_action.html', txtName=txtName)

@app.route('/poem2', methods=['POST'])
def poem2():
    txtName = request.form['txt']
    if txtName == '0':
        file = open("amendments.txt")
    elif txtName == '1':
        file = open("moby_dick.txt")
    elif txtName == '2':
        file = open("aesop.txt")
    elif txtName == '3':
        file = open("beatles.txt")
    elif txtName == '4':
        file = open("bible.txt")
    else:
        file = open("amendments.txt")
    txtName = file.read()
    txtName = markov_poem(txtName)
    return jsonify({"resp" : txtName})

# Run the app :)
if __name__ == '__main__':
    app.run( 
        host="0.0.0.0",
        port=int("80")
    )
