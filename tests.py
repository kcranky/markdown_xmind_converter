# We don't want to do crazy things
#  It may be even simpler than expected


from xmindparser import xmind_to_dict
import json
import markdown


# 1. xmind to dict
test_file = "Chapter 0 - Overview.xmind"
d = xmind_to_dict(test_file)

# Looking at the structure, we have a title - "Sheet 1"
# It has a single topic, which appears to be the central topic on the page.
# This has a title. and a list of topics
# Each topic dict has a title, and a list of topics

# Nested indefinitely as
nest = {
    "title": "Title",
    "topics": [
        {
            "title": "Title"
        }
    ]
}

def xmind_to_markdown(file, dict, level):
    # dict contains as shown above in "nest"
    # level is going to be the level of indentation
    # within a topic, if there are topics, there's a nest
    # print(dict)
    if "topic" in dict.keys():
        # This is a title
        str_to_write = f"# {dict['title']}\n"
        print(str_to_write)
        file.write(str_to_write)
        xmind_to_markdown(file, dict["topic"], level + 1)
    elif "topics" in dict.keys():
        str_to_write = f"{'#' * level} {dict['title']}\n"
        print(str_to_write)
        file.write(str_to_write)
        for topic in dict["topics"]:
            xmind_to_markdown(file, topic, level + 1)
    else:
        # We don't have any keys, and it's just a title, which we write as a singular list
        str_to_write = f"- {dict['title']}\n"
        file.write(str_to_write)
        print(str_to_write)

if __name__ == "__main__":
    with open("output.md", "w+") as f:
        xmind_to_markdown(f, d[0], 0)