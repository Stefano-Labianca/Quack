from convert import markdown_to_html_node

md = """
# Hello `const foo = "bar"`

This is **bolded** paragraph
text in a p
tag here

>Quote _with italic_ and **bold**
>Again quote and `quote`

This is another paragraph with _italic_ text and `code` here

"""

node = markdown_to_html_node(md)

if node != None: 
    print(node.to_html())


# md = """
# ```
# This is text that _should_ remain
# the **same** even with inline stuff
# ```
# """

# node = markdown_to_html_node(md)