import urllib.request
import json
import re

API_URL = "https://victoryanson.com/api/articles?type=blog&limit=5"
README_PATH = "README.md"

def fetch_blogs():
    req = urllib.request.Request(API_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
    return data.get("articles", [])

def generate_markdown_table(blogs):
    if not blogs:
        return "No recent blog posts found."

    table = "| Date | Article | Category | Reading Time |\n"
    table += "| :--- | :--- | :--- | :--- |\n"

    for b in blogs:
        title = b.get("title", "Untitled")
        url = b.get("url", "#")
        date = b.get("date", "")
        badge = b.get("badge", "Blog")
        min_read = f"{b.get('minRead', 1)} min read" if b.get('minRead') else "—"

        table += f"| `{date}` | [{title}]({url}) | `{badge}` | {min_read} |\n"

    return table.strip()

def update_readme(table_content):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"(<!-- BLOG-POSTS:START -->)(.*?)(<!-- BLOG-POSTS:END -->)"
    replacement = f"\\1\n\n{table_content}\n\n\\3"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    blogs = fetch_blogs()
    markdown_table = generate_markdown_table(blogs)
    update_readme(markdown_table)
    print("README.md updated successfully.")
