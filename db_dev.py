import base64
import io
import fitz
from PIL import Image
from langchain_community.document_loaders import PyPDFLoader
import cv2
import numpy as np
from paddleocr import PaddleOCR, PPStructureV3

class doc_tools:

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.ocr = PaddleOCR(lang="id")
        self.pipeline = PPStructureV3(lang="id")

    def pdf_pages_to_base64(self) -> list[str]:
        pdf_document = fitz.open(self.pdf_path)
        base64_pages = []
        
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)  # zero-indexed
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            base64_string = base64.b64encode(buffer.getvalue()).decode("utf-8")
            base64_pages.append(base64_string)
        
        pdf_document.close()  # Good practice to close the document
        return base64_pages
    
    def img_to_markdown(self, img: Image.Image, save_path: str) -> str:
        output = self.pipeline.predict(img)

        for res in output:
            res.save_to_markdown(save_path=save_path)
    

    

if __name__ == "__main__":
    pdf_tool = doc_tools(r"C:\Gabut\journal_entries_sample_1000.pdf")
    img = pdf_tool.img_to_markdown(pdf_tool.pdf_pages_to_base64().decode)
    for i, page in enumerate(pdf_tool.pdf_pages_to_base64()):
        img = base64.b64decode(page)
       
        nparr = np.frombuffer(img, np.uint8)

        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # pdf_tool.img_to_markdown(image, f"output/page_{i+1}.md")
        cv2.imshow(f"page {i+1}", image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()



