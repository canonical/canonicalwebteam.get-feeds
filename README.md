# canonicalwebteam.get-feeds

Functions and template tags for retrieving content from JSON or RSS feeds.

## Installation

``` bash
pip install canonicalwebteam.get-feeds
```

## Usage

Feeds can be loaded either using Python functions or in Django templates:

### Functions

Two functions are provided, which you can use in your views:

``` python
from canonicalwebteam.get_feeds import (
    get_json_feed_content,
    get_rss_feed_content
)

items_dict = get_json_feed_content(
    url="https://example.com/api/items",
    offset=20, # optional
    limit=10 # optional
)
posts_dict = get_json_feed_content(
    url="https://example.com/feed.rss",
    offset=20, # optional
    limit=10, # optional
    exclude_items_in={} # optional
)
```

### Template tags

Or you can include Django templatetags:

``` python
# settings.py

TEMPLATES['OPTIONS']['builtins'].append(
    'canonicalwebteam.get_feeds.templatetags'
)
```

And then get the feed content in templates:

``` html
<h1>Items:</h1>
{% get_json_feed "https://example.com/api/items" limit=10 as items %}
{% if items is False %}
  <p>Feed failed to load</p>
{% else %}
  <ul>{% for item in items %}<li>{{ item.name }}{% endfor %}</ul>
{% endif %}

<h1>Posts:</h1>
{% get_rss_feed "https://example.com/feed.rss" limit=10 as posts %}
{% if items is False %}
  <p>Feed failed to load</p>
{% else %}
<ul>{% for post in posts %}<li>{{ post.title }}{% endfor %}</ul>
{% endif %}
```

