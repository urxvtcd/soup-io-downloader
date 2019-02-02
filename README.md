# Usage

1. Go through all the pages and get content URLs:

```sh
./get_content_urls.py $soup_url > urls
```

The script  logs currently last scrapped  page to `stderr`, you  can use
that if for some reason it fails halfway.

It's possible that you have some content duplication, so run:
```sh
cat urls | sort | uniq > uniq_urls
```

2. Download stuff pointed to by URLs:

```sh
mkdir content_dir
./download_content.py uniq_urls content_dir
```
