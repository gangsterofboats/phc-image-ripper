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
import scrapy

class PhotosSpider(scrapy.Spider):
    name = 'photosspider'

    def __init__(self, search='', *args, **kwargs):
        super(PhotosSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'http://photos.hollywood.com/search/?s={re.sub(" ", "+", search)}']

    def parse(self, response):
        for img in response.css('.imageHolder img'):
            if 'placeholder' in img.css('img').extract_first():
                continue
            image = img.css('img').extract_first()
            image = re.sub('prevcln', 'full', image)
            yield { 'image': image }

        next_page = response.css('div.paginator a.svg-right::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
