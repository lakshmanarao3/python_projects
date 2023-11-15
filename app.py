from flask import Flask, render_template, redirect, request, url_for
from forms import Hostinfo, Subnethost, Subnetsubnets
from calculation import find_hosts, subnet_by_hosts, subnet_by_subnets
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysqxeruuf"

@app.route("/", methods=["GET", "POST"])
def index():
    form = Hostinfo()
    form1 = Subnethost()
    form2 = Subnetsubnets()
    
    if form.validate_on_submit():
        if request.form["form_type"] == 'hostinfo':
            network = form.network.data
            result = find_hosts(network)
            result_json = json.dumps(result)
            return redirect(url_for("host_info", result=result_json))

    if form1.validate_on_submit():
        if request.form["form_type"] == 'subnethost':
            network = form1.network.data
            hosts = form1.hosts.data
            result = subnet_by_hosts(network, hosts)
            return redirect(url_for("subnet_hosts", result=result))

    if form2.validate_on_submit():
        if request.form["form_type"] == "subnetsubnets":
            network = form2.network.data
            subnets = form2.subnets.data
            result = subnet_by_subnets(network, subnets)
            return redirect(url_for("subnet_subnets", result=result))

    return render_template("home.html", form=form, form1=form1, form2=form2)

@app.route("/host_info", methods=["GET", "POST"])
def host_info():
    result_json = request.args.get('result')
    result_dict = {}
    if result_json is None:
        return render_template("host_info.html")
    result_dict = json.loads(result_json)
    return render_template("host_info.html", result=result_dict)

@app.route("/subnet_hosts", methods=["GET", "POST"])
def subnet_hosts():
    result = request.args.getlist('result')
    if result is None:
        return render_template("subnet_hosts.html")
    print(result)
    return render_template("subnet_hosts.html", result=result)

@app.route("/subnet_subnets", methods=["GET", "POST"])
def subnet_subnets():
    result = request.args.getlist('result')
    if result is None:
        return render_template("subnet_subnets.html")
    return render_template("subnet_subnets.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
