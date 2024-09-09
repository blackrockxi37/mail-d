import magic

def get_file_extension(file_path):
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(file_path)
    
    mime_extensions = {
        'text/plain': '.txt',
        'text/html': '.html',
        'application/pdf': '.pdf',
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'application/zip': '.zip',
        'application/msword': '.doc',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        'application/vnd.ms-excel': '.xls',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
        'application/vnd.ms-powerpoint': '.ppt',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
        'application/vnd.openxmlformats-officedocument.presentationml.slideshow': '.ppsx',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.template': '.xltx',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.template': '.dotx',
        'application/vnd.openxmlformats-officedocument.presentationml.template': '.potx',
        'application/vnd.ms-access': '.mdb',
        'application/vnd.visio': '.vsd',
        # добавьте больше MIME-типов по необходимости
    }
    
    # Возвращаем соответствующее расширение
    return mime_extensions.get(mime_type, '')

# Пример использования
file_path = './mails/95/Контрольная работа'
extension = get_file_extension(file_path)
print(f'Определенное расширение: {extension}')
