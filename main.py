from pprint import pprint
import csv
import re


# Читаем адресную книгу в формате CSV в список contacts_list:
with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# pprint(contacts_list)


# ФИО приводим к нужному формату:
phones_book = []
pattern_full_name = r'(^[А-Я]\w+) ?,?(\w+) ?,?(\w+)?'
substitution_pattern_full_name = r'\1,\2,\3'
for i in contacts_list:
    while '' in i:
        i.remove('')
    result = re.sub(pattern_full_name, substitution_pattern_full_name, ','.join(i))
    phones_book.append(result)
# pprint(phones_book)


# Телефонные номера приводим к нужному формату:
pattern_phone_number = r'(\+7|8) ?\(?(\d{3})\)?-? ?(\d{3})\-? ?(\d{2})-? ?(\d{2}) ?\(?(доб\.)? ?(\d+)?(\))?'
substitution_pattern_phone_number = r'+7(\2)\3-\4-\5 \6\7'
for i, j in enumerate(phones_book):
  j = j.split(',')
  result = re.sub(pattern_phone_number,substitution_pattern_phone_number, ','.join(j))
  phones_book[i] = result


phones_book_dict = {}
for _ in phones_book:
    if list(phones_book_dict.keys()).count(','.join(_.split(',')[0:2])):
        phones_book_dict[','.join(_.split(',')[0:2])] += f",{','.join(_.split(',')[2:])}"
    else:
        phones_book_dict.setdefault(','.join(_.split(',')[0:2]), ','.join(_.split(',')[2:]))
      

phones_book_sort = []
for i, j in phones_book_dict.items():
    phones_book_sort.append(list(i.split(',')) + list(j.split(',')))
# pprint(phones_book_sort)


phones_book_final = []
for i in phones_book_sort:
    i = list(dict().fromkeys(i))
    for j in i:
        if j[0] == '+':
            if j.count('доб'):
                i.append(i.pop(i.index(j)))
            else:
                if j.count(' '):
                    i.append(i.pop(i.index(j)).replace(' ', ''))

    for k in i:
        if k.count('@'):
            i.append(i.pop(i.index(k)))
    phones_book_final.append(i)
# pprint(phones_book_final)


with open("phonebook.csv", "w", encoding="utf8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(phones_book_final)





# sorted_list = []
# pattern_final = r'([А-Я]\w+),(\w+),(\w+),(\w+),([А-Яа-яA-za-z –]+)?([0-9\+\(\)-]+ ?\w+\.?\d+)'
# substitution_pattern_final = r'\1,\2,\3,\4,\5,\6'
# for i in phones_book_final:
#     result = re.sub(pattern_final, substitution_pattern_final, ','.join(i))
#     sorted_list.append(result.split(','))
# pprint(sorted_list)


# with open("phonebook.csv", "w", encoding="utf8") as f:
#     datawriter = csv.writer(f, delimiter=',')
#     datawriter.writerows(sorted_list)





# pattern_email = r'([aA-zZ0-9]+)@([a-z0-9]+).([a-z]+)'
# substitution_pattern_email = r'\1@\2.\3'
