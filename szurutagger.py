import deepdanbooru as dd
import szuruAPI as s
import io
import time

# Threshhold at which tags are considered
# Change this to change the threshhold
threshhold = 0.6

model = dd.project.load_model_from_project("pretrained", compile_model = False)

# Needs a project folder under the folder "pretrained"
tags = dd.project.load_tags_from_project("pretrained")

# API limits to 100 posts at a time if there is no limit, so keep trying until there are none left
result = s.getPosts("-tag:bot_tagged,mod_confirmed", 0, fields = "tags,version,id")
while len(result["results"]) < result["total"]:
	result = s.getPosts("-tag:bot_tagged,mod_confirmed", 0)
	posts = result["results"]
	for x in posts:
		oldTags = ["bot_tagged"]
		for category in x["tags"]:
			for tag in category["names"]:
				oldTags.append(tag)
		thumb = s.getThumbnail(x).content
		d = dd.commands.evaluate_image(io.BytesIO(thumb), model, tags, threshhold)
		comment = time.asctime() + "\n"
		postUpdate = { "version": x["version"], "tags": oldTags }
		for tup in d:
			postUpdate["tags"].append(tup[0])
			comment += f"({tup[1]:05.3f}) {tup[0]}\n"
		s.updatePost(x["id"], postUpdate)
		s.createComment(x["id"], comment)