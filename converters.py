import xmind
import json

def xmind_to_markdown(dict, file_handle, indentation, start_bullets=3):
    """
    Writes an xmind dict to a file_handle.
    dict          : The xmind dictionary, created using the xmindparser library
    file_handle   : A handle to an open file opject to which you intend to write to
    indentation   : The intended level of indendation for the current line
    start_bullets : The level of indentation at which to start making a list as opposed to headings
                    3 seems to be the "neatest" for xmind -> markdown due to how I handle nested lists in my xmind files
    """
    if "topic" in dict.keys():
        # This is the title. In most of my books, I don't use this.
        # TODO: Add a check here to see if the name is set.
        xmind_to_markdown(dict["topic"], file_handle, indentation + 1)
    elif "topics" in dict.keys() and indentation < start_bullets:
        # This is a header
        # If a header has a newline, replace the newline with a dash
        header_str = " - ".join(l for l in dict['title'].splitlines() if l)
        # We also insert a newline
        str_to_write = f"\n{'#' * indentation} {header_str}\n"
        file_handle.write(str_to_write)
        for topic in dict["topics"]:
            xmind_to_markdown(topic, file_handle, indentation + 1)
    else:
        # If there's a bullet point with a number, we prevent the auto-formatting of markdown's numbered list
        str_to_write = f"{'    ' * (indentation - start_bullets)}- {dict['title']}\n"
        file_handle.write(str_to_write.replace(".", "\."))
        if "topics" in dict.keys():
            for topic in dict["topics"]:
                xmind_to_markdown(topic, file_handle, indentation + 1)


def remove_keys(dictionary, keys_to_remove = ['id', 'link', 'note', 'label', 'comment', 'markers'] ):
    """
    A method to remove unused keys that xmind provides in it's dict
    We have this so we can check content between conversions.
    I.e. 
        xmind -> dict -> mdown
        mdown -> dict -> xmind
    The dicts should be equal.
    """
    if isinstance(dictionary, dict):
        for k, v in list(dictionary.items()):
            if k in keys_to_remove:
                del dictionary[k]
            else:
                remove_keys(v, keys_to_remove)
    elif isinstance(dictionary, list):
        for item in dictionary:
            remove_keys(item, keys_to_remove)

if __name__ == "__main__":
    # Test the xmind to markdown method
    test_file = "test_docs/Chapter 3 - The Basic Tools.xmind"
    xmind_dict = json.loads(xmind.load(test_file).to_prettify_json())[0]
    remove_keys(xmind_dict)
    with open("xmind_converted_new_dict.md", "w+") as output_file:
        xmind_to_markdown(xmind_dict, output_file, 0)
