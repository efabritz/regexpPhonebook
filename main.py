import re
from pprint import pprint
import csv

def match_phones(entry):
    phone_pattern = r'(\+7|8)?\s*\(?(\d{3})\)?[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})\s*(\(?доб\.\s*(\d+)\)?)?'
    phone_sub = r"+7(\2)\3-\4-\5"
    add_sub = r'+7(\2)\3-\4-\5 доб.\7'

    matched_groups = re.match(phone_pattern,  entry)

    if matched_groups:
        if matched_groups.group(7):
            return re.sub(phone_pattern, add_sub,  entry)
        else:
            return re.sub(phone_pattern, phone_sub,  entry)
    else:
        return entry

def openFile():
    with open("phonebook_raw.csv") as f:
      rows = csv.reader(f, delimiter=",")
      contacts_list = list(rows)
      #pprint(contacts_list)

      formatted_rows = []
      formatted_rows.append(contacts_list[0])

      dict_rows = {}

    for row in contacts_list[1:]:
        fio_div = 1
        for num in range(0, 3):
            entry = row[num]
            entry_list = list(entry.split())

            if len(entry_list) == 1:
                fio_div *= 1
            else:
                fio_div *= 0

        if fio_div == 0:
            fio_united = f'{row[0]} {row[1]} {row[2]}'
            fio_splitted = fio_united.split()
            for elem in range(0, 3):
                if elem < len(fio_splitted):
                    row[elem] = fio_splitted[elem]
                else:
                    row[elem] = ''

        for elem in range(3, len(row)):
            row[elem] = match_phones(row[elem])
        key_check = f'{row[0]}{row[1]}'
        if key_check in dict_rows.keys():
            old_row = dict_rows[key_check]

            if len(row) > len(old_row):
                smallest_length = len(old_row)
            else:
                smallest_length = len(row)
            for r in range(0, smallest_length):
                 if old_row[r] != row[r]:
                    new_entry = old_row[r] + row[r]
                    row[r] = new_entry
        dict_rows[key_check] = row

    contacts_list = list(dict_rows.values())
    formatted_rows += contacts_list

    return formatted_rows

def writePhonebookToCSV(contacts_list):
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


if __name__ == '__main__':
    contacts = openFile()
    writePhonebookToCSV(contacts)

