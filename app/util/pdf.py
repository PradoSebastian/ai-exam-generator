import logging
from datetime import date

from app.integration import MdToPdfClient
from app.constants.agent_constants import (
    API_TEMPLATE_API_KEY,
    API_TEMPLATE_MD_TO_PDF_ENDPOINT,
    API_TEMPLATE_URL,
    RESULTS_PATH,
)
from app.util.path import PathUtil

class PDFUtil:

    EXTENSION = 'pdf'
    MIME_TYPE = 'application/pdf'

    @staticmethod
    def create_pdf_file(text: str, file_name: str = "output") -> None:
        """Creates a PDF file with the specified content."""
        if not API_TEMPLATE_API_KEY:
            logging.error("API Template API key is not set. Cannot create PDF.")
            return
        
        client = MdToPdfClient(
            base_url=API_TEMPLATE_URL,
            md_to_pdf_endpoint=API_TEMPLATE_MD_TO_PDF_ENDPOINT,
            api_key=API_TEMPLATE_API_KEY
        )
        pdf_bytes = client.create_pdf_from_markdown(markdown_content=text, file_name=file_name)
        if pdf_bytes:
            with open(
                PathUtil.get_full_path(RESULTS_PATH) + f"/{file_name}-{date.today()}.{PDFUtil.EXTENSION}", "wb"
            ) as file:
                file.write(pdf_bytes)
            logging.info("Generated PDF saved successfully.")
        else:
            logging.error(f"Failed to generate PDF from markdown, filename: {file_name}.")