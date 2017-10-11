###text_mining.py
import requests
bad_links = ["/wiki/Help","/wiki/File","/wiki/Wiki"]

def find_start(text,start):
	'''
	Finds the start of the body and index 'start' of the wikipedia page represented by 'text'
	'''
	check = text.find("<p>",start)
	if check+5 >= len(text):
		raise ValueError("No appropriate start in string.")
	elif text[check+3:check+5]=="<a" or text[check+3:check+5]=="<s":
		return find_start(text,check+3)
	else:
		return check

def analyze_page(url):
    return requests.get(url).text

def find_link(text,start):
	'''
	Finds and returns the first internal link in 'text' after index 'start' and returns the link.
	This mehtod is very specific to Wikipedia in its parsing.
	'''
	link_start = text.find('href=',start)+6
	link_end = text.find('"',link_start)
	first_link = text[link_start:link_end]
	a = first_link[:5]
	b = first_link[:10]
	if a != "/wiki" or b in bad_links: #insures it is a non-file, non-help internal link
		return find_link(text,link_end)
	else:
		return first_link, link_start+10

def crawl(page,depth,width):

	links = {}
	links_list = []

	text = analyze_page(page)

	for i in range(0,depth):
		next_start = 0
		for j in range(0,width):
			next_link, next_start = find_link(text,find_start(text,next_start))
			if next_link in links:
				#print(next_link)
				#print(links_list)
				break
			else:
				links[next_link] = 1
				links_list.append(next_link)
		text = analyze_page('https://en.wikipedia.org'+next_link)

	print(links_list)

crawl('https://en.wikipedia.org/wiki/Turkish_language', 10, 1)
