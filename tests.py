# We don't want to do crazy things
#  It may be even simpler than expected


from xmindparser import xmind_to_dict
import json
import markdown


# 1. xmind to dict
test_file = "Chapter 3 - The Basic Tools.xmind"
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

# TODO:
# The below solution is sub-optimal as it des not keep a record of the current heading.
# Ideally I think we'd want to keep track (maybe in a list we push and pop to) of the current otem used for indentation.
def xmind_to_markdown(file, dict, level):
    if "topic" in dict.keys():
        # This is the title. In most of my books, I don't use this.
        # TODO: Add a check here to see if the name is set.
        xmind_to_markdown(file, dict["topic"], level + 1)
    elif "topics" in dict.keys():
        # If a header has a newline, replace the newline with a dash
        # TODO implement a max check for header level, after which start indenting more
        header_str = " - ".join(l for l in dict['title'].splitlines() if l)
        str_to_write = f"{'#' * level} {header_str}\n"
        file.write(str_to_write)
        for topic in dict["topics"]:
            xmind_to_markdown(file, topic, level + 1)
    else:
        # We don't have any keys, and it's just a title, which we write as a singular list
        # TODO: When writing out bullet points, don't have them as bullets if they are numbered.
        str_to_write = f"- {dict['title']}\n"
        file.write(str_to_write)

if __name__ == "__main__":
    with open("output.md", "w+") as f:
        xmind_to_markdown(f, d[0], 0)