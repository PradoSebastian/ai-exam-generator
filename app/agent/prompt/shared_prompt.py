MARKDOWN_INSTRUCTION_GENERATION = """
You can reference images using html tags like:
`<img src="`image-url`" width="50">`

Titles must be lower than '###' level, so they can be easily identified as sections of the exam
witout using unnecesary space when converting to PDF (in next steps non applied by you).

Don't include the initial ```markdown and final ``` in the output, just the pure markdown content.
And never include language codes in content.
"""

OUTPUT_FORMAT_INSTRUCTION = """
The output should be a markdown structure that organizes the
content of the images in a clear and structured way. Each image's content 
should be represented ordered in the markdown, and you should use appropriate 
markdown syntax to format and represent the content effectively.
"""