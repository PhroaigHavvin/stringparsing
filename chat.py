import re
import lxml.html
import json
import urllib2

mentionRegEx = r'@\w+'
emoticonRegEx = r'\([a-z0-9]{1,15}\)'
# Source of url regex: http://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
linkRegEx = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

# there are faster ways to do this but this should work for our use case
# just know there are more optimal solutions
def uniquify(sequence):
	"""Make all items in a list unique, keeping order intact.

	input: list of items to make unique

	>>> uniquify([1,1,2,3,1,5,3,4,5])
	[1, 2, 3, 5, 4]
	>>> uniquify([1,3,6,4,7,5])
	[1, 3, 6, 4, 7, 5]
	"""
	unique = []
	for item in sequence:
		if item not in unique:
			unique.append(item)
	return unique


def findMatches(string):
	"""Find all unique matches of @mentions, emoticons using (emotename) notation, and urls including
	their corresponding Title.

	input: string to find all unique matches

	>>> findMatches('@test (hello) http://www.nfl.com')
	{'mentions': ['test'], 'emoticons': ['hello'], 'links': [{'url': 'http://www.nfl.com', 'title': 'NFL.com - Official Site of the National Football League'}]}
	>>> findMatches('@test @test @bob @test (hello) (hello) (hello) (goodbye)')
	{'mentions': ['test', 'bob'], 'emoticons': ['hello', 'goodbye']}
	>>> findMatches('http://www.nfl.com/fakeyfake')
	{'links': [{'url': 'http://www.nfl.com/fakeyfake', 'title': '404 Error - Unable to Load Page'}]}
	>>> findMatches('http://www.iamafakewebsite12345.com/fakeyfake')
	{'links': [{'url': 'http://www.iamafakewebsite12345.com/fakeyfake', 'title': 'Connection Error - Unable to Load Page'}]}
	"""
	results = dict()
	
	mentionMatches = uniquify(re.findall(mentionRegEx, string))

	# if we have any mention matches, put them in a list without the @ symbol
	if len(mentionMatches) > 0:
		results['mentions'] = list()
		for mention in mentionMatches:
			results['mentions'].append(mention[1:])

	emoticonMatches = uniquify(re.findall(emoticonRegEx, string, re.I))

	# if we have any emoticon matches, put them in a list without the enclosing ()
	if len(emoticonMatches) > 0:
		results['emoticons'] = list()
		for emoticon in emoticonMatches:
			results['emoticons'].append(emoticon[1:-1])

	linkMatches = uniquify(re.findall(linkRegEx, string))

	# if we have any link matches, create an array of dictionaries with a title (or error if we cannot get a title)
	if len(linkMatches) > 0:
		results['links'] = list()
		for url in linkMatches:
			title = ''
			try:
				# have to do this do to an IO Error we sometimes get with some versions of lxml
				# this also makes exception handling easier
				page = urllib2.urlopen(url)
				title = lxml.html.parse(page).find(".//title").text
			except urllib2.HTTPError, e:
				title = str(e.code) + ' Error - Unable to Load Page'
			except urllib2.URLError:
				title = 'Connection Error - Unable to Load Page'
			results['links'].append({'url': url,'title': title})

	return results


def getMatchesJSON(string):
	"""Returns JSON data on the matches of a given string.

	input: string to find all unique matches
	"""
	matches = findMatches(string)
	retval = json.dumps(matches, separators=(',', ': '), indent=4)
	return retval

if __name__ == "__main__":
	import doctest
	doctest.testmod()
	text = raw_input('Input a string: ')
	print getMatchesJSON(text)
