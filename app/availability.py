from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas         

# Step 4: The availability algorithm

# Goal: answer the question at the heart of FullChair: “When can this stylist fit a 90-minute silk press on Tuesday?” This is the most interview-worthy part of the project. It’s a classic interval overlap problem, the same idea behind LeetCode questions like Meeting Rooms and Merge Intervals.

# You’ll build it in two layers:

# A pure function that does just the logic: no database, no web. That makes it easy to test and reason about.
# An endpoint that loads the real appointments and calls that function.

# Keeping the logic separate from the database is a design choice worth mentioning in interviews. It’s called separation of concerns.

# Part 1: The key idea, when do two time ranges overlap?

# Picture a booked appointment from 10:00 to 11:00, and a candidate slot you want to check:

# Booked:          |=====10:00–11:00=====|
# Slot A:  |==9:00–10:00==|                      ✓ ends exactly when the booking starts
# Slot B:        |==9:30–10:30==|                ✗ overlaps
# Slot C:                        |==10:30–11:30==|   ✗ overlaps
# Slot D:                         |==11:00–12:00==|  ✓ starts exactly when it ends

# Two ranges overlap if and only if each one starts before the other ends:

# python
# overlaps = slot_start < booked_end and booked_start < slot_end

# That one line is the whole trick. Check it against the picture:

# Slot A: 9:00 < 11:00 is true, but 10:00 < 10:00 is false, so no overlap. Back-to-back appointments are allowed.
# Slot B: 9:30 < 11:00 and 10:00 < 10:30 are both true, so they overlap.

# Most people’s first instinct is to check lots of special cases: starts inside, ends inside, covers completely. This single condition handles all of them, and interviewers love seeing it.

#  List everything it needs to know to answer it. Each of those things becomes a parameter, and the answer becomes the return value.
def available_timeslots(
    new_appt_duration: int

)-> List[tuple[datetime, datetime]]:


