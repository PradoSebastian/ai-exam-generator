MARKDOWN_INSTRUCTION_GENERATION = """
You can reference images using html tags like:
`<img src="`image-url`" width="<50 to 300>" style="<css-styles>">`
For css styles you can play using things like `display: block; margin: 0 auto;` to center an only one image,
but you can include what you consider correct.
For width you can also set a value you consider correct to represent the content image.
If needed you can include <div> tags to represent more complex image aggrupations that can fit well 
with markdown files.
Take into account that inside HTML tags, you can't use markdown syntax, so you should use html tags 
to represent the content, for example bold (**<text>**) should use <strong> tags.

Titles must be lower than '###' level, so they can be easily identified as sections of the exam
witout using unnecesary space when converting to PDF (in next steps non applied by you).
Only first ever title to appear can be '##' level, and the rest of titles must be '###' level or lower, 
so they can be easily identified as sections of the exam when printing.
Avoid duplicating '###' characters, bad example: '### ### Section 1: Kitchen Time with Pokémon! (Verbs & Utensils)'.

Don't include the initial ```markdown and final ``` in the output, just the pure markdown content.
And never include language codes in content.

When adding multiple choise options, you must end the question with a character `\\`, so the options can be rendered
correctly, here is an example:
```
Charmander has wood and matches. He is going to...\\
    a) sleep
    b) light a fire
    c) swim
```

When using matching questions, that reference to images you can use a table to render it properly.
And disorder the options, so it is not that easy to match answers.

Never include a Name/Date section in the result.
"""

OUTPUT_FORMAT_INSTRUCTION = """
The output should be a markdown structure that organizes the
content in a clear and structured way. You should use appropriate 
markdown syntax to format and represent the content effectively.
"""