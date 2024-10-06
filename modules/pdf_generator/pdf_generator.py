from fpdf import FPDF
from io import BytesIO

class PDFGenerator:
    """
    The PDFGenerator class is responsible for creating a PDF document with lyrics and an optional album cover image.

    Attributes:
        None

    Methods:
        create_pdf(lyrics, image) -> BytesIO:
            This method generates a PDF document with the provided lyrics and an optional album cover image.

    Parameters:
        lyrics (str): The lyrics to be included in the PDF document.
        image (PIL.Image.Image, optional): The album cover image to be included in the PDF document. If not provided, the method will not include an image.

    Returns:
        BytesIO: A BytesIO object containing the generated PDF document.
    """
    def create_pdf(self,lyrics, image):
        """
        This method generates a PDF document with the provided lyrics and an optional album cover image.

        Parameters:
            lyrics (str): The lyrics to be included in the PDF document.
            image (PIL.Image.Image, optional): The album cover image to be included in the PDF document. If not provided, the method will not include an image.

        Returns:
            BytesIO: A BytesIO object containing the generated PDF document.
        """
        pdf = FPDF()
        pdf.add_page()

        if image:
            img_path = "album_cover_temp.png"
            image.save(img_path)
            pdf.image(img_path, x=10, y=10, w=100)

        pdf.set_xy(10, 100)
        pdf.set_font("Arial", "B", 12)
        pdf.multi_cell(0, 10, lyrics)

        pdf_output = pdf.output(dest='S').encode('latin1')  
        
        return BytesIO(pdf_output) 
