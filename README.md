# canonicalwebteam.yaml_deleted_paths

Serve `410`s for deleted pages listed in a `deleted.yaml` file.

## Usage

Create `deleted.yaml` similar to the following:

``` yaml
some/path: {"message": "This page is gone!"}
# etc.
```

And a `410.html` template page:

``` html
<html><body><h1>Deleted</h1><p>{{ message }}</p></body></html>
```

And add the module to your Django app:

``` python
# urls.py
from canonicalwebteam import yaml_deleted_paths

urlpatterns = yaml_deleted_paths.create_views()
# ...
```

Now if you visit `http://your-site/some/path` you should see your `410`
error page.
