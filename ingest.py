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

def extract_sections(lines, headers):
    sections = []
    for h in range(len(headers)):
        header_text = headers[h][0]
        header_index = headers[h][1]
        body_start = header_index + 2  #skip past header text + underline

        if h+1 >= len(headers):
            body_end = len(lines) #no next header, so go to the end of the file
        else:
            body_end = headers[h+1][1]  # stop right before the next header starts
        body_lines = lines[body_start : body_end]
        body_text = "\n".join(body_lines).strip()

        sections.append([header_text, body_text])

    return sections



