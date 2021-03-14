import deepdanbooru as dd
import szuruAPI as s
import io

model = dd.project.load_model_from_project("pretrained", compile_model = False)

# Needs a project folder under the folder "pretrained"
tags = dd.project.load_tags_from_project("pretrained")

posts = s.getPosts("-tag:bot_tagged,mod_confirmed", 0)["results"]
for x in posts:
	oldTags = ["bot_tagged"]
	for category in x["tags"]:
		for tag in category["names"]:
			oldTags.append(tag)
	thumb = s.getThumbnail(x).content
	d = dd.commands.evaluate_image(io.BytesIO(thumb), model, tags, 0.5)
	comment = ""
	postUpdate = { "version": x["version"], "tags": oldTags }
	for tup in d:
		postUpdate["tags"].append(tup[0])
		comment += f"({tup[1]:05.3f}) {tup[0]}\n"
	s.updatePost(x["id"], postUpdate)