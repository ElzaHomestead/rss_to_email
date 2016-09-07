import hashlib
import feedparser
import config  # Contains absolute paths

def notify(title,link,subscribers):
	import smtplib
	import email_login  # Contains gmail username and password
	
	# Set message parameters
	gmail_user = email_login.user
	gmail_pwd = email_login.pwd
	FROM = 'Elza Homestead Blog'
	TO = subscribers
	SUBJECT = "New Blog Post - " + title
	TEXT = "Hello subscriber!\n\nThere is a new Elza Homestead blog post: " + title + "\n" + link + "\n\n\n\n---\n\nTo unsubscribe, send a message to admin@elzahomestead.com with \"Unsubscribe\" in the subject line."
	
	# Prepare actual message
	message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
	
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.ehlo()
	server.starttls()
	server.login(gmail_user, gmail_pwd)
	server.sendmail(FROM, TO, message)
	server.close()


# Parse rss feed
posts = feedparser.parse("http://elzahomestead.com/feed.xml")

# Generate list of posts from file
post_list = [line.strip() for line in open(config.posts)]

# Generate MD5 hash for the most current post
lasthash = hashlib.md5(posts.entries[0].guid).hexdigest()

# Check if lasthash is the last post on file, if not notify subscribers
if lasthash != post_list[-1]: 
	subscribers = [sub.strip() for sub in open(config.subs)]
	title = posts.entries[0].title
	link = posts.entries[0].link
	notify(title,link,subscribers)
	with open(config.posts,"a") as posts: posts.write("\n" + lasthash)