import lxml.html as html
from os import getcwd, listdir
file_list = listdir(getcwd() + '/linkedin')
for i in file_list:
    page = html.parse('linkedin/'+i)
    l=page.getroot().find_class('locality')
    p=l[-1].text_content().encode('utf-8').strip()
    s=p.split(',')
    n=page.getroot().find_class('full-name')
    f=n[-1].text_content().encode('utf-8')
    t=f.split()

