import xml.etree.ElementTree as ET
import glob
import string
from collections import Counter
import sqlite3
import os
import logging


class fb2:
    def __init__(self):
        self.path = "C:\\_WRK\\Trainings\\DQE_2020\\PycharmData\\Source"

    # List of fb2 files in Source dir
    def dir_files(self):
        return glob.glob("{}\\*.fb2".format(self.path))

    def get_file_namespace(self):
        return {'fb2': 'http://www.gribuser.ru/xml/fictionbook/2.0'}

    def get_fb2_root(self, filepath):
        document = ET.parse(filepath)
        return document.getroot()

    def get_book_title(self, filepath):
        return self.get_fb2_root(filepath).findall('.//fb2:description/fb2:title-info/fb2:book-title', namespaces=self.get_file_namespace())[0].text

    def get_number_of_paragraphs(self, filepath):
        return len(self.get_list_of_paragraphs(filepath))

    def get_list_of_paragraphs(self, filepath):
        return self.get_fb2_root(filepath).findall('.//*/*/fb2:p', namespaces=self.get_file_namespace())

    def get_number_of_words(self, filepath):
        par_lst = self.get_list_of_paragraphs(filepath)
        count = 0
        for par in par_lst:
            cnt = self.get_p_counter(par)
            count += sum(cnt.values())
        return count

    def get_count_of_unique_words(self, filepath):
        par_lst = self.get_list_of_paragraphs(filepath)
        a = Counter()
        for par in par_lst:
            cnt = self.get_p_counter(par)
            a += cnt
        return a

    def get_count_of_uppercase_words(self, filepath):
        par_lst = self.get_list_of_paragraphs(filepath)
        a = Counter()
        for par in par_lst:
            cnt = self.get_p_counter_uppercase(par)
            a += cnt
        return a

    def get_p_counter(self, par):
        cnt = Counter()
        par_text = par.text
        if par_text is not None:
            translator = par_text.maketrans('', '', string.punctuation)
            word_list = par_text.translate(translator).replace('—', '').replace('…', '').lower().split()
            cnt = Counter(word_list)
        return cnt

    def get_p_counter_uppercase(self, par):
        cnt = Counter()
        par_text = par.text
        if par_text is not None:
            word_list = self.check_is_capitalized(par_text)
            cnt = Counter(word_list)
        return cnt

    def check_is_capitalized(self, par_text):
        translator = par_text.maketrans('', '', string.punctuation)
        word_list = par_text.translate(translator).replace('—', '').replace('…', '').split()
        word_list = list(filter(lambda a: a[0].isupper(), word_list))
        return word_list

    def get_p_number_of_uppercase(self, par):
        cnt = 0
        par_text = par.text
        if par_text is not None:
            word_list = self.check_is_capitalized(par_text)
            for word in word_list:
                if word[0].isupper():
                    cnt += 1
        # info.debug("number of upper case for par #par = cnt")
        return cnt

    def get_number_of_uppercase_words(self, filepath):
        par_lst = self.get_list_of_paragraphs(filepath)
        cnt = 0
        for par in par_lst:
            cnt += self.get_p_number_of_uppercase(par)
        return cnt

    def get_number_of_lowercase_words(self, filepath):
        return self.get_number_of_words(filepath) - self.get_number_of_uppercase_words(filepath)

    def get_number_of_letters(self, filepath):
        par_lst = self.get_list_of_paragraphs(filepath)
        cnt = 0
        for par in par_lst:
            par_text = par.text
            if par_text is not None:
                translator = par_text.maketrans('', '', string.punctuation)
                word_list = par_text.translate(translator).replace('—', '').replace('…', '').replace(' ', '')
            cnt += len(word_list)
        return cnt

    def get_summary_values(self, filepath):
        dict = {}
        dict.update({"file_name": os.path.basename(filepath).split('.')[0]})
        dict.update({"book_name": object_fb2.get_book_title(filepath)})
        dict.update({"number_of_paragraph": object_fb2.get_number_of_paragraphs(filepath)})
        dict.update({"number_of_words": object_fb2.get_number_of_words(filepath)})
        dict.update({"number_of_letters": object_fb2.get_number_of_lowercase_words(filepath)})
        dict.update({"words_with_capital_letters": object_fb2.get_number_of_uppercase_words(filepath)})
        dict.update({"words_in_lowercase": object_fb2.get_number_of_letters(filepath)})
        return dict


class db_util:
    def __init__(self):
        self.db_path = "C:\\_WRK\\Trainings\\DQE_2020\\PycharmData\\Source"
        self.db_name = "Words.db"
        self.db_full_path = self.db_path + "\\" + self.db_name

    def get_file_basename(self, filepath):
        object_fb2 = fb2()
        fb2_list = object_fb2.dir_files()
        lst = []
        for fb2_file in fb2_list:
            lst.append(os.path.basename(fb2_file).split()[0])

    def db_tables_init_statement(self, dbpath, fb2_files):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        # c.execute("DROP TABLE IF EXISTS summary")
        c.execute("CREATE TABLE IF NOT EXISTS summary (file_name text, book_name text, number_of_paragraph integer, number_of_words integer, number_of_letters integer, words_with_capital_letters integer, words_in_lowercase integer)")
        for fb2_file in fb2_files:
            c.execute("DROP TABLE IF EXISTS details_" + os.path.basename(fb2_file).split('.')[0])
            c.execute("CREATE TABLE IF NOT EXISTS details_" + os.path.basename(fb2_file).split('.')[0] + " (word text, count integer, count_uppercase integer)")
        # c.execute("SELECT * FROM details_Example")
        # result = c.fetchall()
        # print(result)
        conn.commit()
        conn.close()

    def db_add_summary(self, dbpath, filepath, dict):
        d = dict.copy()
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        f_name = os.path.basename(fb2_file).split('.')[0]
        c.execute("SELECT count(1) FROM summary WHERE file_name = '" + f_name + "'")
        result = c.fetchone()
        # print("If file record exists in Summary table: result = {}".format(result[0]))
        if result[0] == 0:
            columns = ', '.join(d.keys())
            values = ':' + ', :'.join(d.keys())
            query = 'INSERT INTO summary (%s) VALUES (%s)' % (columns, values)
            c.execute(query, d)
        # c.execute("SELECT * FROM summary")
        # result = c.fetchall()
        # print(result)
        conn.commit()
        conn.close()

    def db_add_details(self, dbpath, all_counts_dict, upper_counts_dict):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        f_name = os.path.basename(fb2_file).split('.')[0]
        for entry in all_counts_dict:
            # print(entry + ": " + str(all_counts_dict[entry]) + " --- " + str(upper_counts_dict[entry.capitalize()]))
            query = "INSERT INTO details_" + f_name + " (word, count, count_uppercase) VALUES (?, ?, ?)"
            c.execute(query, (entry, all_counts_dict[entry], upper_counts_dict[entry.upper()]))
        # .execute("SELECT * FROM details_" + f_name)
        # result = c.fetchall()
        # print(result)
        conn.commit()
        conn.close()


logging.basicConfig(filename="Part1.log", filemode="w", level=logging.INFO)

object_fb2 = fb2()
fb2_list = object_fb2.dir_files()

# print(fb2_list)
logging.info("List of FB2 files to process: {}".format(fb2_list))

object_db_util = db_util()
object_db_util.db_tables_init_statement(object_db_util.db_full_path, fb2_list)

logging.info("Files processing started...")

for fb2_file in fb2_list:
    logging.info("FB2 file name: {}".format(fb2_file))

    # print(object_fb2.get_book_title(fb2_file))
    logging.info("Book title: {}".format(object_fb2.get_book_title(fb2_file)))

    # print(object_fb2.get_number_of_paragraphs(fb2_file))
    logging.info("Number of paragraphs: {}".format(object_fb2.get_number_of_paragraphs(fb2_file)))

    # print(object_fb2.get_number_of_words(fb2_file))
    logging.info("Number of words: {}".format(object_fb2.get_number_of_words(fb2_file)))

    # print(object_fb2.get_number_of_uppercase_words(fb2_file))
    logging.info("Number of UpperCase words: {}".format(object_fb2.get_number_of_uppercase_words(fb2_file)))

    # print(object_fb2.get_number_of_lowercase_words(fb2_file))
    logging.info("Number of LowerCase words: {}".format(object_fb2.get_number_of_lowercase_words(fb2_file)))

    # print(object_fb2.get_number_of_letters(fb2_file))
    logging.info("Number of letters: {}".format(object_fb2.get_number_of_letters(fb2_file)))

    # print(object_fb2.get_summary_values(fb2_file))
    logging.info("Summary: {}".format(object_fb2.get_summary_values(fb2_file)))

    # print(object_fb2.get_count_of_unique_words(fb2_file))
    # logging.info("Book title is: {}".format(object_fb2.get_count_of_unique_words(fb2_file)))

    # print(object_fb2.get_count_of_uppercase_words(fb2_file))
    # logging.info("Book title is: {}".format(object_fb2.get_book_title(fb2_file)))

    logging.info("Adding book Summary to SQLite is started.")
    object_db_util.db_add_summary(object_db_util.db_full_path, fb2_file, object_fb2.get_summary_values(fb2_file))
    logging.info("Adding book Summary to SQLite is completed.")

    logging.info("Adding book Details to SQLite is started.")
    object_db_util.db_add_details(object_db_util.db_full_path, object_fb2.get_count_of_unique_words(fb2_file), object_fb2.get_count_of_uppercase_words(fb2_file))
    logging.info("Adding book Details to SQLite is started.")

    logging.info("End of FB2 file processing.")
