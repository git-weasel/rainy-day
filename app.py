from flask import Flask, render_template, request, redirect


app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

#@app.route('/form')
#def form():
#    return render_template('form.html')
 
#@app.route('/data/', methods = ['POST', 'GET'])
#def data():
#    if request.method == 'GET':
#        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
#    if request.method == 'POST':
#        form_data = request.form
#        return render_template('data.html',form_data = form_data)

if __name__ == '__main__':
  app.run(port=33507)
