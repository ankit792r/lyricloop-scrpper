import os, sys

def bootstrap():
    try:
        target = input("Upload Target [WEB*, DB]: ") or "WEB"
        if target not in ["WEB", "DB"]:
            raise Exception("Invalid upload target.")
        
        target_url = input("Target url: ")
        if not target_url:
            raise Exception("Target url is not provided.")
        
        url_list_file = input("Url list name [url_list.txt*]: ") or "url_list.txt"

        use_cache = False
        if os.path.isfile("temp/data.json"):
            use_cache = (input("use cache data ?: ") != "") or False
        
        return target, target_url, url_list_file, use_cache
    except:
        print("Keyboard interupt")
        sys.exit(1)

def get_urls(file_name):
    urls_list = []
    with open(file_name, "r") as file:
        urls_list = file.read().splitlines()
    return urls_list

def resolve_target(target:str, target_url:str):
    if (target == "WEB"):
        from worker import upload_to_web
        return upload_to_web(url=target_url)
    elif (target == "DB"):
        from worker import upload_to_db
        return upload_to_db(url=target_url)
    else:
        raise Exception("Invalid target.")
