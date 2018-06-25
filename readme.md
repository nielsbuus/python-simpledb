# Python SimpleDB

## The quick story

Simple persistence library with a pretty API that saves lists of dicts into JSON files.

```python
import simpledb

db = simpledb.SimpleDB("/home/joe/dump_it_here")
db.table("jokes").insert(category="political", type="riddle", question="What does Donald Trump tell all his supporters?", answer="Orange Is The New Black.")
db.table("jokes").insert({"category": "computers", "type": "riddle", "question": "Whats the object-oriented way to become wealthy?", "answer": "inheritance"})
db.table("jokes").count()
=> 2
db.table("jokes").where(category="political").count()
=> 1
db.table("jokes").where(category="computers", type="riddle").update(category="software development")
db.table("jokes").insert(foo="bar", id=1234)
db.table("jokes").where(id=1234).delete() # Removes the dict with the foo attribute above.
db.table("jokes").first()
=> trump_joke # Although there is no gaurantee of order.
db.table("jokes").all()
=> [trump_joke, nerd_joke]
db.table("jokes").where(answer="inheritance").all()
=> [nerd_joke]
db.table("jokes").delete() # Removes all jokes.
```

### Pros
- Only 100 lines of Python code.
- No third party dependencies. `json` and `pathlib` which are Python standard libraries.
- Clean simple API
- Creates folders and JSON files automatically
- Persisted data is human readable (it's just JSON)
- Data is kept in memory for reads, so it's (fairly) fast to query (in small quantities).

### Cons
- Very basic feature set
- No optimizations, no indexing. Will slow down as data increases.
- Only works reliably in a single process setup as the data is cached in memory. If your table is loaded in two Python process and you add/update a dictionary in Process 1, then Process 2 will not see it. Worse, if Process 2 adds another dictionary, Process 2 will replace the dictionary added by Process 1.

## The long story

### Background

If you are looking for a Python library that will help you save and load dictionaries from disk without requiring an actual database, this might be for you.

It's basically a convenient encapsulation of JSON files with each file containing a list of objects (dictionaries). Think MongoDB, but very primitive and in-process.

This implementation takes very little code (~100 lines of Python) and probably performs badly as soon as your list exceeds a few megabytes, so the use-case is small self-contained applications that needs to save some settings maybe.

## How to use

    import simpledb

Once imported, you can create a SimpleDB object. The first paramater is the directory to use for persistence. If the directory doesn't exist, SimpleDB will try and create it. If you initialize SimpleDB without a directory, your current working directory will be used.

```python
db = simpledb.SimpleDB("/home/joe/pet_projects/storage")
```

Pick a table to work with.

```python
plant_table = db.table("plants")
```

This will give you a table object that maps to `/home/joe/pet_projects/storage/plants.json`. If that file already exists, SimpleDB will try and load it. If not, SimpleDB won't do anything.

Let's add something.

```python
plant_table.insert(title="Strawberries", genus="Fragaria", pros="Juicy, sweet and beautiful.", cons="Spoils easily. Easily stolen by birds.")
plant_table.insert(title="Raspberries", genus="Rubus", pros="Juicy and delicious. Requires minimal maintenance and weeding.", cons="Prone to beetle attacks.", note="Has a tiny computer named after it. See Raspberry Pi.")
plant_table.insert({"title": "Potatoes", "genus": "Solanum", "pros": Easy to cook", "cons": "If you eat them green, they might kill you.")
```

Although the library uses the term `table` for recognition, there is no schema to be enforced on the objects you insert. Only requirement is that they are passed in as named arguments or a dict and contains variables that Python's JSON library will serialize.

At each `insert`, SimpleDB will serialize and write the list to `plants.json`, so expect slowdown as list size increases.
