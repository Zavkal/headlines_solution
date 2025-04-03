async def generate_text(headline, source_name):
    text = (f'Дата публикации: {headline["date_published"]}\n'
            f'Заголовок: {headline["title"]}\n'
            f'Ссылка: <a href="{headline["url"]}">{source_name}</a>\n')
    return text