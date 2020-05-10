import xml.etree.ElementTree as ET
import glob
import string
from collections import Counter

class fb2:
    def __init__(self):
        self.path = "C:\_WRK\Trainings\DQE_2020\PycharmData\Source"

    # List of fb2 files in Source dir
    def dir_files(self):
        return glob.glob("{}\\Test*.*".format(self.path))

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
            count +=sum(cnt.values())

        return count

    def get_count_of_unique_words(self, filepath):
        par_lst = self.get_list_of_paragraphs(filepath)
        a = Counter()
        for par in par_lst:
            cnt = self.get_p_counter(par)
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
            translator = par_text.maketrans('', '', string.punctuation)
            word_list = par_text.translate(translator).replace('—', '').replace('…', '').split()
            #cnt = Counter(word_list)
            for word in word_list:
                if not word[0].isupper():
                    word_list.remove(word)
        print(type(word_list))
        #return cnt

    def get_p_number_of_uppercase(self, par):
        cnt = 0
        par_text = par.text
        if par_text is not None:
            translator = par_text.maketrans('', '', string.punctuation)
            word_list = par_text.translate(translator).replace('—', '').replace('…', '').split()
            for word in word_list:
                if word[0].isupper():
                    cnt+=1
        return cnt

    def get_number_of_uppercase_words(self, filepath):
        par_lst = self.get_list_of_paragraphs(filepath)
        cnt = 0
        for par in par_lst:
            cnt+=self.get_p_number_of_uppercase(par)
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
            cnt+=len(word_list)
        return cnt

object_fb2 = fb2()
fb2_list = object_fb2.dir_files()

for fb2_file in fb2_list:
    print(fb2_file)
    print(object_fb2.get_book_title(fb2_file))
    print(object_fb2.get_number_of_paragraphs(fb2_file))
    print(object_fb2.get_number_of_words(fb2_file))
    print(object_fb2.get_count_of_unique_words(fb2_file))
    # object_fb2.get_count_of_unique_words(fb2_file)
    print(object_fb2.get_number_of_uppercase_words(fb2_file))
    print(object_fb2.get_number_of_lowercase_words(fb2_file))
    print(object_fb2.get_number_of_letters(fb2_file))


    # for paragraph in object_fb2.get_list_of_paragraphs(fb2_file):
    #     print('')

#number_of_paragraph = len(root.findall('.//fb2:body/*/fb2:p', namespaces=namespace))
#print(number_of_paragraph)
