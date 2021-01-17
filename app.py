from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
	if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
    	return print(form_data)
        form_data = request.form
  return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html',form_data = form_data)
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        return render_template('form.html',form_data = form_data)

if __name__ == '__main__':
  app.run(port=33507)
