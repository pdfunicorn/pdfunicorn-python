pdfunicorn-python
=================

Python client for the PDFUnicorn API (pdfunicorn.com)

    import os
    from pdfunicorn import pdfUnicorn

    API_KEY = os.environ['PDFUNICORN_API_KEY']

    pdfu = pdfUnicorn(api_key=API_KEY)

    image_metadata = self.pdfu.images.create(
        image = 'image/on/disk.jpg',
        src = 'path/to/test_image.jpg'
    )

    pdf_file = self.pdfu.documents.create(
        source = '<doc size="b5"><page><row><cell>Hello World!</cell><cell><img src="path/to/test_image.jpg" /></cell></row></page></doc>',
        pdf = True
    )

    t = open("pdfu_test.pdf", "wb")
    t.write(pdf_file)
    t.close()
