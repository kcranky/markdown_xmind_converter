# We don't want to do crazy things
#  It may be even simpler than expected


from xmindparser import xmind_to_dict
import json
import markdown

# I think we're deciding to not go deeper than 2 headers when going from xmind to markdown
# That means that 

level_maps = ["# ", "## ", "- ", "    - ", "        - "]

# 1. xmind to dict
# test_file = "Chapter 3 - The Basic Tools.xmind"
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

# TODO:
# The below solution is sub-optimal as it does not keep a record of the current heading.
# Ideally I think we'd want to keep track (maybe in a list we push and pop to) of the current otem used for indentation.
def xmind_to_markdown(file, dict, level):
    if "topic" in dict.keys():
        print("top level title")
        # This is the title. In most of my books, I don't use this.
        # TODO: Add a check here to see if the name is set.
        xmind_to_markdown(file, dict["topic"], level + 1)
    elif "topics" in dict.keys() and level < 3:
        # This is a header
        # If a header has a newline, replace the newline with a dash
        header_str = " - ".join(l for l in dict['title'].splitlines() if l)
        # We also insert a newline
        str_to_write = f"\n{'#' * level} {header_str}\n"
        print(f"header is {str_to_write}")
        file.write(str_to_write)
        for topic in dict["topics"]:
            xmind_to_markdown(file, topic, level + 1)
    else:
        # We don't have any keys, and it's just a title, which we write as a singular list
        # If there's a bullet point with a number, we exclude markdowns auto-formatting of numbered lists.
        # We also know that at this point, it could be a part of a nested list, which means we need to handle
        str_to_write = f"{'    ' * (level-3)}- {dict['title']}\n"
        file.write(str_to_write.replace(".", "\."))
        if "topics" in dict.keys():
            for topic in dict["topics"]:
                xmind_to_markdown(file, topic, level + 1)

if __name__ == "__main__":
    with open("output.md", "w+") as f:
        xmind_to_markdown(f, d[0], 0)