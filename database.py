import sqlite3
conn = sqlite3.connect("recipes.db")
curr = conn.cursor()
curr.execute("""
    CREATE TABLE IF NOT EXISTS recipe_ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_name TEXT,
        ingredient TEXT,
        calories REAL,
        protein REAL,
        carbs REAL,
        fat REAL,
        date TEXT DEFAULT (DATE('now'))
   )
""")
conn.commit()
conn.close()
