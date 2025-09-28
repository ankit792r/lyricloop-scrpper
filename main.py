from database import Database
from link import extract_links
from data import extract_data

db = Database()
extract_data(db)
db.close_db()

