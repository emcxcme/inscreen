def greet_user(id: int, first_name: str) -> str:
    text = "Hello po Ka. <a href='tg://user?id=%s'>%s</a>!" % (id, first_name)
    return text
