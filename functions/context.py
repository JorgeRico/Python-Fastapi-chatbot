import json

CONTEXT_FILE   = "./context_files/context.json"

# load context from json file
def load_context():
    try:
        with open(CONTEXT_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# update context file
def update_context(role, message):
    context = load_context()
    context.append(set_role_context(role, message))
    save_context(context)

# save context file
def save_context(context):
    with open(CONTEXT_FILE, "w", encoding="utf-8") as file:
        json.dump(context, file, ensure_ascii=False, indent=4)

# reset context file
def reset_context(role, initial_context = "Talk like a pirate. Max 2 paragraphs"):
    context = set_role_context(role, initial_context)
    save_context([context])

# set role context object
def set_role_context(role, content):
    return {
        "role": role,
        "content": content
    }