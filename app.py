
import os
from flask import Flask, render_template,url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cities import miestai
from menu import menu


app = Flask(__name__)

# Prisijungiam prie duomenų bazės
basedir = os.path.abspath(os.path.dirname(__file__))
app.app_context().push() 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Klasės modelis kuriame nurodyta kaip mes dirbsime su duomenu baze.
class company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.TEXT(50), nullable = False)
    code = db.Column(db.Integer, nullable = False)
    vat = db.Column(db.TEXT(14), nullable = True)
    adress = db.Column(db.TEXT(50), nullable = False)
    company_bank_name = db.Column(db.TEXT(50), nullable = False)
    company_bank_swift = db.Column(db.TEXT(15), nullable = False)
    company_bank_iban = db.Column(db.TEXT(50), nullable = False)

    def __init__(self, name, code, vat, adress, company_bank_name,company_bank_swift,company_bank_iban):
    
        self.name = name
        self.code = code
        self.vat = vat
        self.adress = adress
        self.company_bank_name = company_bank_name
        self.company_bank_swift = company_bank_swift
        self. company_bank_iban = company_bank_iban

    def __repr__(self):
        return f'{self.name} {self.code} {self.vat} {self.adress} {self.company_bank_name} {self.company_bank_swift} {self.company_bank_iban}'

# kelias pagal kurį atidarysime pagrindį puslapį
@app.route("/", methods=['GET', 'POST'])

# atsirenkame duomenis iš duomenų bazės ir atidarome indeksinį html failą kuriame bus pradžia tinklapio ir persiunčiame visus duomenis kad juos galėtume panaudoti
def index():
    # pasiemam visus duomenis išskyrus id
    comp =  company.query.order_by(company.name.desc()).with_entities(
    company.name,
    company.code,
    company.vat,
    company.adress,
    company.company_bank_name,
    company.company_bank_swift,
    company.company_bank_iban
    ).all()
    return render_template('index.html', menu=menu, comp = comp)

# kelias pagal kurį atidarysime puslapį kuriame yra bus companijų pridejimo formą
@app.route("/company", methods=['GET', 'POST'])

# Aprašoma funkciją kur priskiriame kuriuos duomenis pridėsime į duomenų bazę
def add_company():
    
    if request.method == 'POST' and request.form:
        company_name = request.form['company_name']
        company_code = request.form['company_code']
        company_vat = request.form['company_vat']
        company_adress = request.form['company_adress']
        company_bank_name = request.form['company_bank_name']
        company_bank_swift = request.form['company_bank_swift']
        company_bank_iban = request.form['company_bank_iban']

        comp = company(name=company_name, code = company_code, vat = company_vat, adress = company_adress, company_bank_name = company_bank_name, company_bank_swift = company_bank_swift, company_bank_iban = company_bank_iban) 
        
        try:
            db.session.add(comp)
            db.session.commit()
            return redirect('/')
        except:
            return "Error adding company"
        
    else:
        return render_template('company.html', menu=menu)

# kelias į puslapį kuriame bus išvestas comapinų sąrašas esantis duomenų bazėje
@app.route("/company_list", methods=['GET'])

# Funkcija kurioje aprašoma kokie duomenis bus paimti iš duomenų bazės ir 
def company_list():
    # pasiemam visus duomenis išskyrus id
    comp =  company.query.order_by(company.name.desc()).with_entities(
    company.name,
    company.code,
    company.vat,
    company.adress,
    company.company_bank_name,
    company.company_bank_swift,
    company.company_bank_iban
    ).all()
    return render_template('company_list.html', menu=menu, comp = comp)

if __name__ == '__main__':
    app.run(debug=True)

