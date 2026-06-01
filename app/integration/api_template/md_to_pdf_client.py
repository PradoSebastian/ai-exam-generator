import json
import requests
from typing import Any


class MdToPdfClient:
    def __init__(
            self,
            base_url: str,
            md_to_pdf_endpoint: str,
            api_key: str,
        ):
        self.base_url = base_url
        self.md_to_pdf_endpoint = md_to_pdf_endpoint
        self.api_key = api_key

    def _create_data_body(self, markdown_text: str) -> dict[str, Any]:
        return {
            "body": markdown_text,
            "data": {
                "lang": "Markdown"
            },
            "settings": {
                "paper_size": "A4",
                "orientation": "1",
                "header_font_size": "9px",
                "margin_top": "10",
                "margin_right": "20",
                "margin_bottom": "20",
                "margin_left": "10",
                "print_background": "1",
                "displayHeaderFooter": False,
            }
        }

    def _create_headers(self) -> dict[str, Any]:
        return {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

    def _create_query_params(self, file_name: str) -> dict[str, Any]:
        return {
            #"expiration": 5,
            "export_type": "file",
            "filename": file_name
        }

    def create_pdf_from_markdown(
            self,
            markdown_content: str,
            file_name: str
        ) -> bytes:
        body = self._create_data_body(markdown_content)
        headers = self._create_headers()
        query_params = self._create_query_params(file_name)
        response = requests.post(
            url=f"{self.base_url}{self.md_to_pdf_endpoint}",
            headers=headers,
            json=body,
            params=query_params
        )

        if response.status_code == 200:
            result = response.content

        return result
            
            
            