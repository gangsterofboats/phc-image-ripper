#!/usr/bin/env python
#################################################################################
# Photos.Hollywood.Com Ripper                                                   #
# Copyright (C) 2018 Michael Wiseman                                            #
#                                                                               #
# This program is free software: you can redistribute it and/or modify it under #
# the terms of the GNU General Public License as published by the Free Software #
# Foundation, either version 3 of the License, or (at your option) any later    #
# version.                                                                      #
#                                                                               #
# This program is distributed in the hope that it will be useful, but WITHOUT   #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS #
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more        #
# details.                                                                      #
#                                                                               #
# You should have received a copy of the GNU General Public License along with  #
# this program.  If not, see <https://www.gnu.org/licenses/>.                   #
#################################################################################

import re
import requests
import sys
from bs4 import BeautifulSoup

arg = ' '.join(sys.argv[1:])
file_name = '-'.join(sys.argv[1:]) + '.html'
search = '+'.join(sys.argv[1:])
uri = f'http://photos.hollywood.com/search/?s={search}'
doc = requests.get(uri).text
content = BeautifulSoup(doc, 'lxml')

fh = open(file_name, 'w')
fh.write(f'<h1>{arg}</h1>\n')
fh.write('<h2>Page 1</h2>\n')

lp = content.select('.search-description')
last_page = re.search(r'\d+$', lp[0].contents[0])[0]
results = content.select('.imageHolder img')
for i in results:
    if 'placeholder' in str(i):
        continue
    image = str(i)
    image = re.sub('prevcln', 'full', image)
    fh.write(f'{image}\n')

for page in range(2, int(last_page) + 1):
    fh.write(f'<h2>Page {page}</h2>\n')
    uri = f'http://photos.hollywood.com/search/?s={search}&p={page}'
    doc = requests.get(uri).text
    content = BeautifulSoup(doc, 'lxml')
    rs = content.select('.imageHolder img')

    for r in rs:
        if 'placeholder' in str(i):
            continue
        image = str(i)
        image = re.sub('prevcln', 'full', image)
        fh.write(f'{image}\n')
fh.close()
