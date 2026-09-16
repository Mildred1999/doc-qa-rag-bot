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


