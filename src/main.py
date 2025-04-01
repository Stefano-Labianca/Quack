import re
from markdown_scanner.block_scanner import block_to_block_type, markdown_to_blocks


md = """
This should
all be
one match

# this should match heading

### this should also match heading

1. one 
2. two 
3. three 

- one
- two
- three

> Star quote block
> Another quote

this should be a second match
Another paragrah

and again

```
const foo = "bar"
```
"""
blocks = markdown_to_blocks(md)


for block in blocks:
    print(f"'{block}'")
    print(block_to_block_type(block))
    print("----------")

