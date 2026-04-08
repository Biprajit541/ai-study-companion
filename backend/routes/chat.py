from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from services.llm import generate_response
from pypdf import PdfReader

router = APIRouter()

# In-memory storage
document_text = ""

class ChatRequest(BaseModel):
    messages: list


# 📄 Upload document
@router.post("/upload-doc")
async def upload_doc(file: UploadFile = File(...)):
    global document_text

    try:
        if file.filename.endswith(".pdf"):
            reader = PdfReader(file.file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            document_text = text
        else:
            content = await file.read()
            document_text = content.decode("utf-8")

        return {"message": "Document uploaded successfully"}

    except Exception as e:
        return {"message": f"Upload failed: {str(e)}"}


# 💬 Chat with memory + document
@router.post("/chat")
def chat(req: ChatRequest):
    global document_text

    try:
        messages = req.messages

        # Inject document context
        if document_text:
            messages = [
                {
                    "role": "system",
                    "content": f"""
You are an AI tutor.

Use the uploaded document if relevant.
If the answer is not in the document, use general knowledge.

Document:
{document_text[:3000]}
"""
                }
            ] + messages[1:]

        answer = generate_response(messages)
        return {"response": answer}

    except Exception as e:
        return {"response": f"⚠️ Error: {str(e)}"}
