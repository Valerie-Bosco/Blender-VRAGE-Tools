import bpy

def wrap_text(text: str, width: int):
    """Returns a list of strings, formatted to a specified width"""

    lines = text.splitlines()
    lines_new = []

    for l in lines:
        if len(l) > width:
            temp = l[:width]
            space_idx = temp.rfind(" ")
            if temp.rfind("\\") > space_idx:
                space_idx = temp.rfind("\\") + 1
            lines_new.append(l[:space_idx])

            overflow = l[space_idx:]
            if overflow.startswith(" ") and not overflow.startswith("  "):
                overflow = overflow[1:]
            lines_new.insert(len(lines_new), overflow)
        else:
            lines_new.append(l)

    return lines_new