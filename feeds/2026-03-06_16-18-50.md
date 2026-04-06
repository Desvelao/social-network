---
title: markdown support and test variable interpolation
date: 2026-03-06T16:18:50Z
link: {{ gh_repo_source_base_url }}/{{ file_path }}
use_html_content: yes
image: https://images2.alphacoders.com/479/thumb-350-479565.webp
my_var: VAR from metadata
---
# Markdown Features Sample

## Headings
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6

## Emphasis
- *Italic*
- **Bold**
- ***Bold & Italic***
- ~~Strikethrough~~

## Lists
### Unordered List
- Item A
- Item B
  - Nested item

### Ordered List
1. First
2. Second
3. Third

## Links
[Microsoft](https://www.microsoft.com)

## Images
![Alt text](image-url)

## Code
Inline code: `print("Hello")`

Code block:
```python
def greet():
  return "Hello"
```

## Blockquotes
> This is a blockquote.

## Tables
| Product | Price | Stock |
|---------|--------|--------|
| Pen     | 1€     | Yes    |
| Notebook| 3€     | No     |

## Horizontal Rule
---

## Task Lists
- [x] Add markdown features
- [ ] Review
- [ ] Finalize

## Escaping Characters
Use `\*` to show a literal asterisk.

## Footnotes
Here is a sentence with a footnote.[^1]

[^1]: This is the footnote text.

## Inline HTML
<p>This is an inline HTML example.</p>


![Image](https://images2.alphacoders.com/479/thumb-350-479565.webp)

Más info en [mi web](https://ejemplo.com)

Testing template string:

my_var: {{ my_var }}

file_path: {{ file_path }}

file_name: {{ file_name }}

file_dir: {{ file_dir }}

file_ext: {{ file_ext }}

gh_repo_source_base_url: {{ gh_repo_source_base_url }}

gh_owner: {{ gh_owner }}

gh_repo: {{ gh_repo }}

gh_pages_base_url: {{ gh_pages_base_url }}

gh_repo_source_base_url: {{ gh_repo_source_base_url }}
