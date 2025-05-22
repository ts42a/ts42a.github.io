#!/usr/bin/env python3
import json
import os
import datetime
import re

# Resolve paths so this script can live in "…/ts42a.github.io/data"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_FILE = os.path.join(SCRIPT_DIR, 'posts.json')
BLOGS_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'blogs'))

def ensure_blogs_dir():
    """Ensure the blogs directory exists."""
    os.makedirs(BLOGS_DIR, exist_ok=True)

def load_posts():
    """Load posts list from the JSON store."""
    if not os.path.exists(POSTS_FILE):
        return []
    with open(POSTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_posts(posts):
    """Save posts list to the JSON store."""
    with open(POSTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

def slugify(text):
    """Turn heading text into a filesystem-safe slug."""
    s = re.sub(r'[^0-9a-zA-Z]+', '_', text).strip('_')
    return re.sub(r'_+', '_', s)

def create_html(post):
    ensure_blogs_dir()

    share_url = f"https://ts42a.github.io/blogs/{post['filename']}"
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{post['heading']}</title>

  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">
  <!-- Font Awesome -->
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet" crossorigin="anonymous">
  <!-- Custom CSS -->
  <link rel="stylesheet" href="../src/css/style.css">
  <link rel="stylesheet" href="../src/css/blog.css">
</head>
<body>
  <!-- Navbar -->
  <nav class="navbar fixed-top bg-transparent">
    <div class="container">
      <div class="row w-100 align-items-center">
        <div class="col-md-5 d-flex justify-content-start">
          <ul class="navbar-nav flex-row mb-0 gap-4">
            <li class="nav-item"><a class="nav-link" href="../index.html">Home</a></li>
            <li class="nav-item"><a class="nav-link" href="../portfolio.html">Portfolio</a></li>
            <li class="nav-item"><a class="nav-link" href="../blog.html">Blog</a></li>
            <li class="nav-item"><a class="nav-link" href="../about.html">About</a></li>
            <li class="nav-item"><a class="nav-link" href="../contact.html">Contact</a></li>
          </ul>
        </div>
        <div class="col-md-2 text-center">
          <a class="navbar-brand logo fw-bold" href="#">TS42<span class="text-accent">a</span></a>
        </div>
        <div class="col-md-5 d-flex justify-content-end align-items-center gap-4 social-icons">
          <a href="https://github.com/ts42a" aria-label="GitHub"><i class="fab fa-github fa-lg"></i></a>
          <a href="#" aria-label="Twitter"><i class="fab fa-twitter fa-lg"></i></a>
          <a href="https://www.linkedin.com/in/tonmoy42a/" aria-label="LinkedIn"><i class="fab fa-linkedin fa-lg"></i></a>
        </div>
      </div>
    </div>
  </nav>

  <section class="container blog-content" style="padding-top: 12vh; padding-bottom: 12vh; margin-top: 50px; margin-bottom: 50px; padding: 20px; max-width: 900px; margin-left: auto; margin-right: auto;" >
    <h2 class="text-center mb-2 fw-bold pt-5">{post['heading']}</h2>
    <p class="text-center mb-5">{post['date']} <strong class="text-accent">|</strong> {post['time']}</p>
    <div>{post['content']}</div>

        <!-- SHARE BUTTONS -->
    <div class="share-buttons text-center my-4">
      <a href="https://twitter.com/share?url={share_url}&text={post['heading']}" target="_blank" class="btn btn-outline-primary me-2">
        <i class="fab fa-twitter"></i> Tweet
      </a>
      <a href="https://www.facebook.com/sharer/sharer.php?u={share_url}" target="_blank" class="btn btn-outline-primary">
        <i class="fab fa-facebook"></i> Share
      </a>
    </div>

    <!-- AUTHOR INFO -->
    <div class="author text-center mt-4">
      <p>Written by <strong>Tonmoy Sarker</strong></p>
    </div>
  </section>


  <!-- Footer -->
  <footer class="py-3 text-center bg-dark text-white">
    <div class="container">
      <small>© 2025 Tonmoy Sarker. All rights reserved.</small>
    </div>
  </footer>

   <script src="../src/fuc/index.js"></script>
</body>
</html>
"""
    html_path = os.path.join(BLOGS_DIR, post['filename'])
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

def list_posts(posts):
    """Print a summary of all saved posts."""
    if not posts:
        print("No posts found.")
        return
    print("\nExisting Posts:")
    for p in posts:
        print(f"ID: {p['id']}  |  {p['heading']}  |  {p['date']} {p['time']}")
    print()

def add_post(posts):
    """Prompt user to add a new post, save JSON and HTML."""
    heading = input("Heading: ").strip()
    content = input("Content (HTML allowed): ").strip()
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%H:%M:%S')
    slug = slugify(heading)
    filename = f"{slug}_{now.strftime('%Y%m%d_%H%M%S')}.html"
    post_id = max((p['id'] for p in posts), default=0) + 1
    post = {
        'id': post_id,
        'heading': heading,
        'content': content,
        'date': date,
        'time': time,
        'filename': filename
    }
    posts.append(post)
    save_posts(posts)
    create_html(post)
    print(f"Post added (ID={post_id}), HTML written to {os.path.join(BLOGS_DIR, filename)}.")

def edit_post(posts):
    """Prompt user to edit an existing post, then update JSON and HTML."""
    list_posts(posts)
    try:
        pid = int(input("Enter ID of post to edit: "))
    except ValueError:
        print("Invalid ID.")
        return
    post = next((p for p in posts if p['id'] == pid), None)
    if not post:
        print("Post not found.")
        return
    new_heading = input(f"New heading (leave blank to keep '{post['heading']}'): ").strip()
    new_content = input("New content (leave blank to keep existing): ").strip()
    if new_heading:
        post['heading'] = new_heading
    if new_content:
        post['content'] = new_content
    now = datetime.datetime.now()
    post['date'] = now.strftime('%Y-%m-%d')
    post['time'] = now.strftime('%H:%M:%S')
    slug = slugify(post['heading'])
    post['filename'] = f"{slug}_{now.strftime('%Y%m%d_%H%M%S')}.html"
    save_posts(posts)
    create_html(post)
    print(f"Post ID {pid} updated, HTML regenerated as {os.path.join(BLOGS_DIR, post['filename'])}.")

def delete_post(posts):
    """Prompt user to delete a post, remove from JSON and delete HTML file."""
    list_posts(posts)
    try:
        pid = int(input("Enter ID of post to delete: "))
    except ValueError:
        print("Invalid ID.")
        return
    idx = next((i for i, p in enumerate(posts) if p['id'] == pid), None)
    if idx is None:
        print("Post not found.")
        return
    filename = posts[idx]['filename']
    html_path = os.path.join(BLOGS_DIR, filename)
    confirm = input(f"Delete post ID {pid}? This will also delete {html_path}. (y/N): ").strip().lower()
    if confirm == 'y':
        posts.pop(idx)
        save_posts(posts)
        if os.path.exists(html_path):
            os.remove(html_path)
        print(f"Post ID {pid} and file {html_path} deleted.")
    else:
        print("Aborted.")

def main():
    """Main loop: offer menu to add, edit, delete, list, or exit."""
    actions = {
        '1': ('Add new post', add_post),
        '2': ('Edit existing post', edit_post),
        '3': ('Delete a post', delete_post),
        '4': ('List all posts', lambda ps: list_posts(ps)),
        '5': ('Exit', None)
    }
    posts = load_posts()
    while True:
        print("\n=== Blog Manager ===")
        for k, (desc, _) in actions.items():
            print(f"{k}. {desc}")
        choice = input("Choose an option: ").strip()
        if choice == '5':
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action[1](posts)
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main()
