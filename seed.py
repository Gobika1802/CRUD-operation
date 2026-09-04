"""Seed script – inserts 50 sample students into your Supabase 'students' table.

Run once:  python seed.py

Make sure the table exists in Supabase with columns:
  id        bigint (primary key, generated always as identity)
  name      text
  email     text
  age       integer
  course    text
"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Sai",
    "Rohan", "Vihaan", "Krishna", "Ishaan", "Shaurya",
    "Diya", "Ananya", "Priya", "Neha", "Kavya",
    "Aadhya", "Sneha", "Riya", "Pooja", "Meera",
    "Rahul", "Kiran", "Manoj", "Deepak", "Sanjay",
    "Pooja", "Sunita", "Divya", "Swati", "Nisha",
    "Akash", "Nikhil", "Tarun", "Varun", "Amit",
    "Shruti", "Pallavi", "Jaya", "Lakshmi", "Geeta",
    "Rajan", "Pradeep", "Suresh", "Mohan", "Vinod",
    "Komal", "Rekha", "Suman", "Alka", "Usha",
]

COURSES = [
    "Computer Science", "Mathematics", "Physics", "Chemistry",
    "Biology", "English Literature", "Economics", "Commerce",
    "Mechanical Engineering", "Electrical Engineering",
]

students = []
for i in range(50):
    first = FIRST_NAMES[i % len(FIRST_NAMES)]
    last = f"Student{i + 1:02d}"
    students.append({
        "name": f"{first} {last}",
        "email": f"{first.lower()}{i+1:02d}@college.edu",
        "age": 18 + (i % 8),
        "course": COURSES[i % len(COURSES)],
    })

print(f"Inserting {len(students)} students …")

# Batch insert (Supabase Python client inserts rows list in one call)
supabase.table("students").insert(students).execute()

print("Done!")
