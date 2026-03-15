import streamlit as st
import json
import os

# File to store notes
NOTES_FILE = "notes.json"


def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return {}


def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)


st.set_page_config(page_title="Notes App", page_icon="📝", layout="centered")
st.title("📝 My Notes App")


if 'notes' not in st.session_state:
    st.session_state.notes = load_notes()


st.subheader("Add a New Note")
col1, col2 = st.columns([2,1])
note_title = col1.text_input("Title")
category = col2.text_input("Category (optional)")
note_content = st.text_area("Content")

if st.button("Add Note"):
    if note_title and note_content:
        st.session_state.notes[note_title] = {"content": note_content, "category": category}
        save_notes(st.session_state.notes)
        st.success(f"Note '{note_title}' added!")
    
        st.experimental_set_query_params()  # refreshes inputs
    else:
        st.error("Both title and content are required.")


st.subheader("Search Notes")
search_term = st.text_input("Search by title or content")
filtered_notes = {title:data for title,data in st.session_state.notes.items() if search_term.lower() in title.lower() or search_term.lower() in data["content"].lower()}


st.subheader("Your Notes")
if filtered_notes:
    for title, data in filtered_notes.items():
        st.markdown(f"**Title:** {title}")
        st.markdown(f"**Category:** {data['category'] if data['category'] else 'None'}")
        st.write(data['content'])
        if st.button(f"Delete '{title}'"):
            st.session_state.notes.pop(title)
            save_notes(st.session_state.notes)
            st.success(f"Note '{title}' deleted!")
else:
    st.info("No notes found. Add a new note or adjust your search.")
