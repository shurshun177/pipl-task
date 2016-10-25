import lxml.html as html
from collections import OrderedDict
import json
from os import listdir, getcwd, path, remove
from powton import states

log = {'locality': 0, 'city': 0, 'state': 0, 'country': 0, 'name': 0, 'first': 0, 'last': 0, 'middle': 0}
error_dict = {'indexError': 0, 'parseError': 0}

def parse(filename):
    try:
        from lxml.etree import ParseError

        page = html.parse('linkedin/' + filename)
        locality = page.getroot().find_class('locality').pop().text_content().encode('utf-8').strip()
        locality_list = locality.split(',')

        log['locality'] += 1
        locale_dict = OrderedDict()
        if len(locality_list) == 1:
            if 'Area' in locality_list[0]:
                city = locality_list[0]
                locale_dict['city'] = city
                log['city'] += 1
            else:
                country = locality_list[0]
                locale_dict['country'] = country
                log['country'] += 1
        elif len(locality_list) == 2:
            city = locality_list[0]
            locale_dict['city'] = city
            log['city'] += 1
            locale_dict['state'] = ''
            for s in states:
                if s in locality_list[1]:
                    state = locality_list[1]
                    locale_dict['state'] = state
                    log['state'] += 1

            if not locale_dict['state']:
                country = locality_list[1]
                locale_dict['country'] = country
                log['country'] += 1
        elif len(locality_list) == 3:
            city = locality_list[0]
            state = locality_list[1]
            country = locality_list[2]
            locale_dict = OrderedDict([('city', city), ('state', state), ('country', country)])
            log['city'] += 1
            log['state'] += 1
            log['country'] += 1

        name = page.getroot().find_class('full-name').pop()
        log['name'] += 1
        full = name.getchildren()[0].text_content().encode('utf-8').split()
        middle = ''
        if len(full) == 2:
            middle = full[1]
            log['middle'] += 1
        first = full[0]
        log['first'] += 1
        last = name.getchildren()[1].text_content().encode('utf-8')
        log['last'] += 1
        name_dict = OrderedDict([('firstName', first), ('middleName', middle), ('lastName', last)])
        final_dict = OrderedDict([('name', name_dict), ('location', locale_dict)])
        f = 'output/' + filename[:-5] + '.json'
        if path.exists(f):
            remove(f)
        output = open(f, 'a')
        output.write(json.dumps(final_dict, indent=2, ensure_ascii=False))
        output.close()
    except ParseError:
        error_dict['parseError'] = 'bad html in ' + filename
    except IndexError:
        error_dict['indexError'] = 'no locality tag in ' + filename


def saveLog():
    f = 'log.txt'
    if path.exists(f):
        remove(f)
    output_log = open(f, 'a')
    output_log.write(json.dumps(error_dict, indent=2, ensure_ascii=False))
    output_log.write(json.dumps(log, indent=2, ensure_ascii=False))
    output_log.close()


file_list = listdir(getcwd() + '/linkedin')
for i in file_list: parse(i)
saveLog()
