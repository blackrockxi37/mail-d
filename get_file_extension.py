import magic

def get_file_extension(file_path):
    # Создаем объект Magic для определения MIME-типа
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(file_path)
    
    # Словарь для сопоставления MIME-типов с расширениями
    mime_extensions = {
        'text/plain': '.txt',
        'text/html': '.html',
        'application/pdf': '.pdf',
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'application/zip': '.zip',
        # добавьте больше MIME-типов по необходимости
    }
    
    # Возвращаем соответствующее расширение
    return mime_extensions.get(mime_type, '')