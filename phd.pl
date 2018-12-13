#!/usr/bin/env ruby
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

require 'nokogiri'
require 'open-uri'

arg = ARGV.join(' ')
file_name = ARGV.join('-') + '.html'
search = ARGV.join('+')
doc = Nokogiri::HTML(open("http://photos.hollywood.com/search/?s=#{search}"))

fh = File.open(file_name, 'w+')
fh.puts("<h1>#{arg}</h1>")
fh.puts('<h2>Page 1</h2>')

lp = doc.css('.search-description')
last_page = lp.first.content.match(/\d+$/)[0]

results = doc.css('.imageHolder img')
results.each do |i|
  next if i.to_s.include? 'placeholder'
  image = i.to_s
  image.sub!(/prevcln/, 'full')
  fh.puts(image)
end

(2..last_page.to_i).each do |page|
  fh.puts("<h2>Page #{page}</h2>")
  content = Nokogiri::HTML(open("http://photos.hollywood.com/search/?s=#{search}&p=#{page}"))

  rs = content.css('.imageHolder img')
  rs.each do |r|
    next if r.to_s.include? 'placeholder'
    img = r.to_s
    img.sub!(/prevcln/, 'full')
    fh.puts(img)
  end
end
fh.close
