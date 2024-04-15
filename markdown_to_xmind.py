import xmind


def get_md_dict(file):
    """
    Return a dict created from the markdown file, in the same format used
    """
    return NotImplementedError


def dict_to_xmind(outfile, dict):
    workbook = xmind.load(outfile)
    sheet1 = workbook.getPrimarySheet()
    root_topic1 = sheet1.getRootTopic()
    root_topic1.setTitle(dict["topic"]["title"])
    for topic in dict["topic"]["topics"]:
        add_xmind_branch(root_topic1, topic)
    xmind.save(workbook, path=outfile)


def add_xmind_branch(root_topic, dict):
    new_root = root_topic.addSubTopic()
    new_root.setTitle(dict["title"])
    if "topics" in dict.keys():
        for topic in dict["topics"]:
            add_xmind_branch(new_root, topic)


if __name__ == "__main__":
    test_file = ""
    xmind_dict = get_md_dict(test_file)
    dict_to_xmind("out_test.md", xmind_dict)
