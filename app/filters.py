from . import app

@app.template_filter('decimate')
def decimate(number):
    if number == None:
        return '0.00'
    else:
        return "{:.2f}".format(float(number))