from ast import dump
from turtle import title
from unicodedata import category
from application import app, db
from flask import render_template, flash, redirect, url_for, get_flashed_messages
from application.form import UserInputForm
from application.models import IncomeExpenses
import json

@app.route("/")
def index():
    entries = IncomeExpenses.query.order_by(IncomeExpenses.date.desc()).all()
    return render_template('index.html', title='index', entries=entries)


@app.route("/add", methods = ['GET', 'POST'])
def add_expense():
    form = UserInputForm()
    if form.validate_on_submit():
        entry = IncomeExpenses(type = form.type.data, amount = form.amount.data,
                                category=form.category.data)
        db.session.add(entry)
        db.session.commit()
        flash('Successful entry',"success")
        return redirect(url_for('index'))

    return render_template('add.html', title='add', form=form)


@app.route('/delete/<int:entry_id>')
def delete(entry_id):
    entry = IncomeExpenses.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Deletion was success",'sucess' )
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    income_vs_expenses = db.session.query(db.func.sum(IncomeExpenses.amount),
        IncomeExpenses.type).group_by(IncomeExpenses.type).order_by(IncomeExpenses.type).all()

    dates = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.date).group_by(IncomeExpenses.date).order_by(IncomeExpenses.date).all()

    categories = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.category).group_by(IncomeExpenses.category).order_by(IncomeExpenses.category).all()

    income_expense = []
    for total_amount, _ in income_vs_expenses:
            income_expense.append(total_amount)

    over_time_expenditure = []
    dates_labels = []
    for amount,date in dates:
        over_time_expenditure.append(amount)
        dates_labels.append(date.strftime("%m-%d-%Y"))
    
    catamount = []
    for amount, category in categories:
        catamount.append(amount)

    return render_template('dashboard.html', 
                        income_vs_expenses =json.dumps(income_expense), 
                        over_time_expenditure = json.dumps(over_time_expenditure),
                        dates_labels = json.dumps(dates_labels),
                        catamount = json.dumps(catamount)
                        )