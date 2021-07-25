import sqlite3
import random


def user_bill_id(user_id):
    try:
        with sqlite3.connect("db.sqlite") as con:
            cur = con.cursor()
            result = cur.execute('SELECT * FROM `bill_id` WHERE `user_id` = ?', (user_id,)).fetchall()
            boolean = bool(len(result))
            if (boolean == True):
                for row in result:
                    return row[1]
            else:
                return 0
    except:
        pass


def get_sub(iduser):
    try:
        with sqlite3.connect("db.sqlite") as con:
            cur = con.cursor()
            result = cur.execute('SELECT * FROM `users` WHERE `iduser` = ?', (iduser,)).fetchall()
            for row in result:
                return row[3]
    except:
        return 0


def user_balance(iduser):
    try:
        with sqlite3.connect("db.sqlite") as con:
            cur = con.cursor()
            result = cur.execute('SELECT * FROM `users` WHERE `iduser` = ?', (iduser,)).fetchall()
            for row in result:
                return row[1]
    except:
        return 0


def user_update_balance(iduser, value):
    try:
        balance = user_balance(iduser) + value
        with sqlite3.connect("db.sqlite") as con:
            cur = con.cursor()
            cur.execute("UPDATE `users` SET `balance` = ? WHERE `iduser` = ?", (balance, iduser))
    except:
        pass


def user_un_balance(iduser, value):
    try:
        balance = user_balance(iduser) - value
        with sqlite3.connect("db.sqlite") as con:
            cur = con.cursor()
            cur.execute("UPDATE `users` SET `balance` = ? WHERE `iduser` = ?", (balance, iduser))
    except:
        pass


def user_wins(iduser):
    try:
        with sqlite3.connect("db.sqlite") as con:
            cur = con.cursor()
            result = cur.execute('SELECT * FROM `users` WHERE `iduser` = ?', (iduser,)).fetchall()
            for row in result:
                return row[2]
    except:
        return 0


def user_update_wins(iduser, value):
    try:
        wins = user_wins(iduser) + value
        with sqlite3.connect("db.sqlite") as con:
            cur = con.cursor()
            cur.execute("UPDATE `users` SET `wins` = ? WHERE `iduser` = ?", (wins, iduser))
    except:
        pass


def add_refill(pay_id, user_id, amount):
    with sqlite3.connect("db.sqlite") as db:
        db.execute("INSERT INTO storage_refill (pay_id, user_id, amount) VALUES (?, ?, ?)",
                   [pay_id, user_id, amount])
        db.commit()
