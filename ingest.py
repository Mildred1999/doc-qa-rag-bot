from pathlib import Path

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
        return sections

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




