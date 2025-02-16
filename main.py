from utils import get_urls, bootstrap, resolve_target
from worker import scrap_data

if __name__ == "__main__":
    target, target_url, url_list_file, use_cache = bootstrap()

    if not use_cache:
        url_lists = get_urls(url_list_file)

        scrap_data(url_list=url_lists)

    result = resolve_target(target, target_url)

    if result:
        print("Uploaded successfully.")
    else:
        print("Failed to upload")


