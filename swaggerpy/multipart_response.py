from uuid import uuid4
from swaggerpy import http_client


def add_lines(name, content, is_file, boundary, lines):
    """Add content to lines with proper format needed for multipart
    content type.

    :param name: name of the request parameter
    :param content: contents of the request parameter
    :param is_file: is the parameter a file type (for adding filename)
    :param boundary: a string to be added after each request param
    :param lines: content array being populated
    :return: updated content array
    """
    header = "Content-Disposition: form-data; name={0}".format(name)
    if is_file:
        header += "; filename={0}".format(name)
    lines.extend(["--" + boundary, header, "", content])
    return lines


def get_random_boundary():
    """A simple boundary generator
    """
    return uuid4().hex


def create_multipart_content(request_params, headers):
    boundary = get_random_boundary()
    lines = []

    # Add all form fields
    for k, v in request_params.get('data', {}).items():
        add_lines(k, v, False, boundary, lines)

    # Add all form files
    for file_name, f in request_params['files'].items():
        add_lines(file_name, f.read(), True, boundary, lines)

    lines.extend(["--" + boundary + "--", ""])
    content_type = http_client.MULT_FORM + "; boundary={0}".format(boundary)
    # Skip 'content-length' as it is generated by BodyProducer
    headers['content-type'] = content_type
    return "\r\n".join(lines)
