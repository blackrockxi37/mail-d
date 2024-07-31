import mimetypes

def get_file_extension(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    
    mime_extensions = {
        'text/plain': '.txt',
        'text/html': '.html',
        'application/pdf': '.pdf',
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'application/zip': '.zip',
        'application/msword': '.doc',  # Word 97-2003
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',  # Word
        'application/vnd.ms-excel': '.xls',  # Excel 97-2003
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',  # Excel
        'application/vnd.ms-powerpoint': '.ppt',  # PowerPoint 97-2003
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',  # PowerPoint
        'application/vnd.openxmlformats-officedocument.presentationml.slideshow': '.ppsx',  # PowerPoint Slideshow
        'application/vnd.openxmlformats-officedocument.spreadsheetml.template': '.xltx',  # Excel Template
        'application/vnd.openxmlformats-officedocument.wordprocessingml.template': '.dotx',  # Word Template
        'application/vnd.openxmlformats-officedocument.presentationml.template': '.potx',  # PowerPoint Template
        'application/vnd.ms-access': '.mdb',  # Microsoft Access
        'application/vnd.visio': '.vsd',  # Microsoft Visio
        # добавьте больше MIME-типов по необходимости
    }
    
    return mime_extensions.get(mime_type, '')

# Пример использования
file_path = './mails/95/Контрольная работа.docx'
extension = get_file_extension(file_path)
print(f'Определенное расширение: {extension}')


