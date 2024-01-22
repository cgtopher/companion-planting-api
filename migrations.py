MIGRATIONS = [
    "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Plant) REQUIRE p.name IS UNIQUE",
    "MERGE (:Category { type: 'veg', name: 'Vegetable'})",
    "MERGE (:Category { type: 'hrb', name: 'Herb'})"
]

