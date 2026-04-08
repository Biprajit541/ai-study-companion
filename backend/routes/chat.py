from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from services.llm import generate_response
from pypdf import PdfReader

router = APIRouter()

# 🧠 Store document in memory
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
        else:
            content = await file.read()
            text = content.decode("utf-8")

        # Limit size (important)
        document_text = text[:5000]

        return {"message": "Document uploaded successfully"}

    except Exception as e:
        return {"message": f"Error: {str(e)}"}


# 💬 Chat (lightweight RAG)
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

Use the document below to answer.
If not found, say you don’t know.

Document:
{document_text}
"""
                }
            ] + messages[1:]

        answer = generate_response(messages)

        return {"response": answer}

    except Exception as e:
        return {"response": f"⚠️ Error: {str(e)}"}
