"""Nurillayev Xurshid""" 

import datetime
import sqlite3


db = sqlite3.connect('databese.db')


def hozirgivaqt():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def jadvalkirit(database, jadval_nomi, ustun):
    try:
        jadvallar = jadvallsit(database)
        cursor = database.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {jadval_nomi} ({ustun}) ''')
        database.commit()
        if jadval_nomi not in jadvallar:
            return f"{jadval_nomi} jadvali yaratildi"
        else:
            return f"{jadval_nomi} jadvali oldin yaratilgan"
    except Exception as e:
        return f"Xatolik: {e}"


def jadvallsit(database):
    try:
        cs = database.cursor()
        cs.execute("SELECT name FROM sqlite_master WHERE type='table';")
        jadvallar = cs.fetchall()
        cs.close()
        return [jadval[0] for jadval in jadvallar]
    except Exception as e:
        return f"Xatolik: {e}"


def ustunkirit(database, jadval_nomi, **ustun_nomi):
    try:
        natija = ""
        ustunlar = ustunlist(database, jadval_nomi)
        cs = database.cursor()
        for kalit, qiymat in ustun_nomi.items():
            if kalit in ustunlar:
                natija = natija + f"{kalit} ustuni avval yaratilgan "
            else:
                cs.execute(f'''ALTER TABLE {jadval_nomi} ADD COLUMN
            {kalit} {qiymat}''')
                natija = natija + f"{kalit} ustuni qo'shildi"
        database.commit()
        cs.close()
        return natija
    except Exception as e:
        return f"Xatolik: {e}"


def ustunlist(database, jadval_nomi):
    try:
        ustunnomi = []
        jadvallar = jadvallsit(database)
        if jadval_nomi in jadvallar:
            cs = database.cursor()
            cs.execute(f'''PRAGMA table_info({jadval_nomi})''')
            ustunnomi = [column[1] for column in cs.fetchall()]
            cs.close()
        else:
            ustunnomi.append(f"{jadval_nomi} jadvali mavjud emas")
        return ustunnomi
    except Exception as e:
        return f"Xatolik: {e}"


def deletetable(database, jadval_nomi):
    try:
        jadvallar = jadvallsit(database)
        cs = database.cursor()
        if jadval_nomi in jadvallar:
            cs.execute(f'''DROP TABLE {jadval_nomi}''')
            database.commit()
            cs.close()
            return f"{jadval_nomi} jadvali muvoffaqqiyatli o'chirildi"
        else:
            cs.close()
            return f"{jadval_nomi} jadvali mavjud emas!"
    except Exception as e:
        return f"Xatolik: {e}"


def deleteustun(database, jadval_nomi, *ustun_nomi):
    try:
        jadvallar = jadvallsit(database)
        ustunlar = ustunlist(database, jadval_nomi)
        if jadval_nomi in jadvallar:
            cs = database.cursor()
            for key in ustun_nomi:
                if key in ustunlar:
                    cs.execute(f'''ALTER TABLE {jadval_nomi} DROP COLUMN {key}''')
                    print(f"{jadval_nomi} jadvalidan {key} ustuni o'chirildi!")
                else:
                    print(f"{jadval_nomi} jadvalida {ustun_nomi} ustuni mavjud emas")
        database.commit()
    except Exception as e:
        return f"Xatolik: {e}"


def jadvalnitoldir(database, jadval_nomi, **ustun_qiymat):
    jadvallar = jadvallsit(database)
    ustunlarlist = ""
    qiymatlar = ""
    i = 1
    try:
        if jadval_nomi in jadvallar:
            for kalit, qiymat in ustun_qiymat.items():
                if len(ustun_qiymat) > 1 and i != 1:
                    ustunlarlist = ustunlarlist + f", {kalit}"
                    if type(qiymat).__name__ == "str":
                        qiymatlar = qiymatlar + f", \"{qiymat}\""
                    else:
                        qiymatlar = qiymatlar + f", {qiymat}"
                else:
                    ustunlarlist = f"{kalit}"
                    qiymatlar = f"{qiymat}"
                    i = 2
        querystr = f"INSERT INTO {jadval_nomi} ({ustunlarlist}) VALUES ({qiymatlar})"

        cs = database.cursor()
        cs.execute(querystr)
        cs.close()
        database.commit()
        return f"Malumotlar saqlandi ✅"
    except Exception as e:
        return f"xatolik: {e}"


def jadvaldanolish(database, jadval_nomi, *ustun_nomi):
    try:
        i = 1
        qstr = ""
        if ustun_nomi[0] == "":
            query = f"SELECT * FROM {jadval_nomi}"
        else:
            for ustun in ustun_nomi:
                if len(ustun_nomi) > 1 and i != 1:
                    qstr = f"{qstr}, " + f"{ustun}"
                else:
                    qstr = f"{ustun}"
                    i = i + 1
            query = f"SELECT {qstr} FROM {jadval_nomi}"
        cs = database.cursor()
        cs.execute(query)
        malumotlar = cs.fetchall()
        cs.close()
        return malumotlar
    except Exception as e:
        return f"Xatolik: {e}"


def ustunqidir(database, jadval_nomi, ustun_nomi, shart):
    try:
        cs = database.cursor()
        if ustun_nomi and shart:
            query = f"SELECT {ustun_nomi} FROM {jadval_nomi} WHERE {shart}"
        elif ustun_nomi:
            query = f"SELECT {ustun_nomi} FROM {jadval_nomi}"
        else:
            query = f"SELECT * FROM {jadval_nomi}"
        print(f"USTUNQIDIR QUERY: {query}")
        cs.execute(query)
        malumot = cs.fetchall()
        cs.close()
        return malumot

    except Exception as e:
        print(f"USTUNQIDIR XATOLIK: {e}")
        return []


def satrni_ochirish(database, jadval_nomi, shart):
    try:
        query = f"DELETE FROM {jadval_nomi} WHERE {shart}"
        cs = database.cursor()
        cs.execute(query)
        database.commit()
        cs.close()
        return f"{jadval_nomi}dan {shart} bo'lgan satr o'chirildi ✅"
    except Exception as e:
        return f"Xatolik: {e}"


def malumotuzgartir(database, jadval_nomi, ustun_nomi, qiymat, shart):
    try:
        query = f"UPDATE {jadval_nomi} SET {ustun_nomi} = {qiymat} WHERE {shart}"
        cs = database.cursor()
        cs.execute(query)
        database.commit()
        cs.close()
        return f"ma'lumot saqlandi ✅"
    except Exception as e:
        return f"Xatolik: {e}"
