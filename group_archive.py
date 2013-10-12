import urllib2
import json
import iso8601

filename = "posts.csv"

url_jaamroom = "https://graph.facebook.com/<INSERT GROUP ID HERE>/feed?access_token=<INSER ACCESS TOKEN HERE>"

def parse_date(datestring):
	if(datestring == None):
		return ["None","None"]
	else:
		datetimestring = iso8601.parse_date(datestring).strftime('%Y-%m-%d %H:%M:%S')
		return datetimestring.split()


def sane(text, quotes=True):
	if(quotes):
		return text.encode('ascii','ignore').replace('"','')

def get_likes(post_data):
	likes_count = 0
	if post_data.get('likes') != None:
		likes_count = len(post_data.get('likes').get('data'))
	return likes_count

def get_comments(post_data):
	comment_count = 0
	if post_data.get('comments') != None:
		comment_count = len(post_data.get('comments').get('data'))
	return comment_count

def fetch_post(url_for_group,file_handler):
	data = urllib2.urlopen(url_for_group).read()
	jsondata = json.loads(data)
	for i,post in enumerate(jsondata['data']):
		author_name = sane(post.get('from').get('name'))
		m = post.get('message')
		if(m == None):
			message = "None"
		else:
			message = " ".join(m.split())
		likes = get_likes(post)
		comments = get_comments(post)
		updated_on = parse_date(post.get('updated_time'))
		file_handler.write(author_name + ";" + message + ";" + str(likes) + ";" + str(comments) + ";" + updated_on[0] + ";" + updated_on[1] + '\n')
		print "Done"
	
def indexing(url):
	file_handle = open(filename,'w')
	while(url is not None):
		fetch_post(url,file_handle)
		page = urllib2.urlopen(url).read()
		data = json.loads(page)
		if(data.get('paging') is not None):
			url = data.get('paging').get('next')
			print url
		else:
			print "Reached last page. Done."
			file_handle.close()
			break

if __name__ == "__main__":
	indexing(url_jaamroom)




	

