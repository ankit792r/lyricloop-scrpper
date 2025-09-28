import sys

from dotenv import load_dotenv

from data import extract_data
from database import Database
from link import extract_links

if __name__ == "__main__":
    load_dotenv()
    db = Database()
    if len(sys.argv) == 1:
        print("action not specified")
        sys.exit(0)

    if sys.argv[1] == "links":
        try:
            from_page = int(sys.argv[2])
            to_page = int(sys.argv[3])
        except IndexError:
            print("FROM and TO page must be specified")
            sys.exit(0)
        extract_links(db_instance=db, from_page=from_page, to_page=to_page)

    elif sys.argv[1] == "data":
        artist_page_limit = 2
        try:
            artist_page_limit = int(sys.argv[2])
        except IndexError:
            pass

        extract_data(db_instance=db, limit=artist_page_limit)

    else:
        print("unknown action specified")
        sys.exit(0)