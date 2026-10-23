from pathlib import Path
import re
import random

def find_files(root_dir):
    file_paths = []
    for path in Path(root_dir).rglob("*"):
        if path.suffix in [".md", ".rst"]:
            file_paths.append(path)

    return file_paths

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

        if filepath.suffix == ".rst":
            headers = find_rst_headers(lines)
            header_line_count = 2
        elif filepath.suffix == ".md":
            headers = find_markdown_headers(lines)
            header_line_count = 1
        else:
            raise ValueError(f"Unsupported file type: {filepath.suffix}")

        sections = extract_sections(lines, headers, header_line_count)
        clean_sections = []
        for section in sections:
            section[1] = clean_text(section[1])
            if section[1].strip() != '':
                clean_sections.append(section)
        return clean_sections

def chunk_text(text, max_words, overlap_words):
    words = text.split()
    if len(words) <= max_words:
        return[text]
    
    chunks = []
    step = max_words - overlap_words
    start = 0
    while start < len(words):
        end = start + max_words
        piece_words = words[start:end]
        chunk = " ".join(piece_words)
        chunks.append(chunk)
        if end >= len(words):
            break
        start += step
    return chunks

def build_chunks(root_dir):
    all_chunks = []
    file_paths = find_files(root_dir)
    for filepath in file_paths:
        source = filepath.relative_to(root_dir).as_posix()
        sections = process_file(filepath)

        for section_number, section in enumerate(sections):
            header = section[0]
            body = section[1]
            pieces = chunk_text(body, 150, 30)

            for piece_number, piece in enumerate(pieces):
                full_text = f"{header}\n{piece}"
                chunk_id = f"{source}::{section_number}::{piece_number}"
                all_chunks.append({"id": chunk_id, "text": full_text, "source": source, "section": header, "chunk_index": piece_number})
    return all_chunks

def find_rst_headers(lines):
    headers = []
    for i in range(len(lines)):
        cur_line = lines[i].strip()

        if cur_line == "": continue

        # check if last line before peeking ahead
        if i+1 < len(lines):
            next_line = lines[i+1].strip()
            if next_line != "" and len(next_line) >= len(cur_line) and len(set(next_line)) == 1 and next_line[0] in ["=", "-", "~", "^", '"', "'", "\\", ".", "*", "+", "#", ":"]:
                headers.append([cur_line, i])

    return headers

def extract_sections(lines, headers, header_line_count):
    sections = []
    for h in range(len(headers)):
        header_text = headers[h][0]
        header_index = headers[h][1]
        body_start = header_index + header_line_count  #skip past header text + underline if rst

        if h+1 >= len(headers):
            body_end = len(lines) #no next header, so go to the end of the file
        else:
            body_end = headers[h+1][1]  # stop right before the next header starts
        body_lines = lines[body_start : body_end]
        body_text = "\n".join(body_lines).strip()

        sections.append([header_text, body_text])

    return sections

def find_markdown_headers(lines):
    headers = []
    for i in range(len(lines)):
        cur_line = lines[i]
        if cur_line == "":
            continue
        if cur_line.startswith("#"):
            level = len(cur_line) - len(cur_line.lstrip("#"))
            header_text = cur_line.strip().strip("#").strip()
            headers.append([header_text, i, level])
    return headers

def clean_text(text):
    #split text into individual lines
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("::: "):
            continue
        elif re.match(r"^:\w+:(\s|$)", stripped_line):
            continue
        elif stripped_line.startswith("..") and "::" in stripped_line:
            continue
        elif stripped_line.startswith("!!!"):
            continue
        else:
            stripped_line = re.sub(r":ref:`([^<]+)<[^>]+>`", r"\1", stripped_line)
            stripped_line = re.sub(r"\*\*(.+?)\*\*", r"\1", stripped_line)
            stripped_line = re.sub(r"\*([^\s*][^*]*?)\*", r"\1", stripped_line)
            cleaned_lines.append(stripped_line)
        
    cleaned_text = "\n".join(cleaned_lines)
    cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text) #remove extra new lines
    cleaned_text = re.sub(r" {2,}", " ", cleaned_text) # remove extra spaces
    cleaned_text = cleaned_text.strip()
    return cleaned_text

if __name__ == "__main__":
    chunks = build_chunks("data/raw")

    if not chunks:
        print("No chunks were built. Check that data/raw has .rst or .md files.")
    else:
        print(f"Built {len(chunks)} chunks from the documents.")
        word_counts = [len(chunk["text"].split()) for chunk in chunks]
        print("Average chunk length:", sum(word_counts) / len(word_counts))
        print("Word count for largest chunk:", max(word_counts))

        for chunk in random.sample(chunks, min(3, len(chunks))):
            print("---")
            print(chunk["id"])
            print(chunk["text"])