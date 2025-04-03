async def generate_text(headline, source_name):
    try:
        text = (f'Дата публикации: \n{headline["date_published"]}\n'
                f'Заголовок: \n{headline["title"]}\n'
                f'Ссылка: <a href="{headline["url"]}">{source_name}</a>\n')
    except Exception:
        text = (f'Дата публикации: \n{headline.date_published.strftime('%Y-%m-%d %H:%M')}\n'
                f'Заголовок: \n{headline.title}\n'
                f'Ссылка: <a href="{headline.url}">{source_name}</a>\n')
    return text