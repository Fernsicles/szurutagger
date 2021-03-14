import requests
import json

config = json.load(open("config.json"))

# Returns a search result resource as a python dict
def getPosts(query = "", count = 0, offset = 0):
	if(count <= 0):
		count = ""
	url = config["url"] + "/api/posts/?offset=" + str(offset) + "&limit=" + str(count) + "&query=" + query
	posts = requests.get(url, headers = {"Accept": "application/json"}, auth=requests.auth.HTTPBasicAuth(config["user"], config["password"]))
	return posts.json()

# Takes in the post id as a number and the post update object as a dict
# Returns the status given
def updatePost(id, post):
	url = config["url"] + "/api/post/" + str(id)
	header = {"Accept": "application/json", "Content-Type": "application/json"}
	return requests.put(url, headers = header, data = json.dumps(post), auth=requests.auth.HTTPBasicAuth(config["user"], config["password"]))

def createComment(comment):
	url = config["url"] + "/api/comments/"
	header = {"Accept": "application/json", "Content-Type": "application/json"}
	return requests.post(url, headers = header, data = json.dumps(comment), auth=requests.auth.HTTPBasicAuth(config["user"], config["password"]))

# Takes a post resource and returns the response
def getThumbnail(post):
	url = config["url"] + "/" + post["thumbnailUrl"]
	return requests.get(url)