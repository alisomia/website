import re



def transform_markdown_to_html(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as md_file:
        markdown_content = md_file.read()

    # Regular expression to match each entry in the Markdown file
    entry_pattern = re.compile(r'\d+\.\s*(.*?)\n\s*-\s*(.*?)\s*\n\s*-\s*(.*?)\s*\n\s*-\s*(.*?)\s*\n\s*-\s*(.*?)\s*\n\s*-\s*(.*?)$', re.MULTILINE | re.DOTALL)

    # Find all entries
    entries = entry_pattern.findall(markdown_content)

    with open(output_file, 'w', encoding='utf-8') as html_file:
        html_file.write(f'''---
title: Research 
date: 2021-10-11 16:10:18
mathjax: true

---
<post-body style="line-height: 1.3"> 

All authors are listed in alphabetical order unless otherwise specified.
''')

        i = 0
        for entry in entries:
            title = entry[0]
            journal = entry[1]
            journal = re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',journal)
            authors = entry[2]
            authors = re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',authors)
            info = entry[3]
            link_arxiv = entry[4]
            link_arxiv = re.sub(r'arxiv:\s*(.*?)\s*', r'\1',link_arxiv)
            link_published = entry[5]
            matches = re.findall(r'(.*?):\s?(.*)',link_published)
            jrnl_name = matches[0][0]
            jrnl_link = matches[0][1]

            html_content = html_format(title, journal, authors, info, link_arxiv, jrnl_link, jrnl_name)
            # Write the HTML content to the output file
            html_file.write(html_content + '\n')
            i+=1
            print(f'Article {i} formatted!')


    print(f'Transformation completed. HTML saved to {output_file}')


def link_format(link,style,name):
    return f'''<div style="margin:0px;"><a href="{link}"><{style}>&nbsp;{name}&nbsp;</{style}></a></div><br>\n'''

def html_format(title, journal, authors, info, link_arxiv, link_published, jrnl_name):
    link_part = f''''''
    if link_published != '':
        link_part = link_part + link_format(link_published,'jrnl',jrnl_name)
    if link_arxiv != '' :
        link_part = link_part + link_format(link_arxiv, 'arxiv','arxiv')

    html_content = f'''
<div class="container">
   <div class="article">
      {title}<br>
      <info>{journal}</info><br>
      <info>{authors}</info>  
   </div>
   <div class="link">
      {link_part}
   </div>
</div>
'''
    return html_content

# Example usage:
input_markdown_file = './source/research/articles.md'
output_html_file = './source/research/index2.md'
transform_markdown_to_html(input_markdown_file, output_html_file)