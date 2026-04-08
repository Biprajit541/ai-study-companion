from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from services.llm import generate_response
from services.vector_store import add_documents, search
from utils.text_splitter import split_text
from pypdf import PdfReader

router = APIRouter()

class ChatRequest(BaseModel):
    messages: list


# 📄 Upload + process document
@router.post("/upload-doc")
async def upload_doc(file: UploadFile = File(...)):
    try:
        if file.filename.endswith(".pdf"):
            reader = PdfReader(file.file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
        else:
            content = await file.read()
            text = content.decode("utf-8")

        chunks = split_text(text)
        add_documents(chunks)

        return {"message": "Document indexed successfully"}

    except Exception as e:
        return {"message": f"Error: {str(e)}"}


# 💬 Chat with RAG
@router.post("/chat")
def chat(req: ChatRequest):
    try:
        messages = req.messages
        user_question = messages[-1]["content"]

        # 🔍 Retrieve relevant chunks
        relevant_chunks = search(user_question, k=5)

        context = "\n\n".join(relevant_chunks)

        messages = [
            {
                "role": "system",
                "content": f"""
You are an AI tutor.

Use the context below to answer clearly.
If the answer is not found, say you don’t know.

Context:
{context}
"""
            }
        ] + messages[1:]

        answer = generate_response(messages)

        return {"response": answer}

    except Exception as e:
        return {"response": f"⚠️ Error: {str(e)}"}
