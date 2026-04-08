from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from services.llm import generate_response
from pypdf import PdfReader

router = APIRouter()

# 🧠 Store chunks with page info
document_chunks = []

class ChatRequest(BaseModel):
    messages: list


# ✂️ Split text into chunks WITH page numbers
def split_text_with_pages(reader, chunk_size=1200, overlap=200):
    chunks = []

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text() or ""

        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i+chunk_size]

            chunks.append({
                "text": chunk,
                "page": page_num + 1
            })

    return chunks


# 📄 Upload document
@router.post("/upload-doc")
async def upload_doc(file: UploadFile = File(...)):
    global document_chunks

    try:
        if file.filename.endswith(".pdf"):
            reader = PdfReader(file.file)
            document_chunks = split_text_with_pages(reader)

        else:
            content = await file.read()
            text = content.decode("utf-8")

            # fallback (no page numbers)
            document_chunks = [{
                "text": text,
                "page": 1
            }]

        return {
            "message": f"Processed {len(document_chunks)} chunks from document"
        }

    except Exception as e:
        return {"message": f"Error: {str(e)}"}


# 🔍 Score chunks
def score_chunk(chunk_text, query):
    score = 0
    for word in query.lower().split():
        score += chunk_text.lower().count(word)
    return score


# 🔍 Retrieve best chunks
def get_relevant_chunks(query, k=5):
    scored = []

    for chunk in document_chunks:
        s = score_chunk(chunk["text"], query)
        if s > 0:
            scored.append((s, chunk))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [chunk for _, chunk in scored[:k]]


# 💬 Chat with citations
@router.post("/chat")
def chat(req: ChatRequest):
    global document_chunks

    try:
        messages = req.messages
        question = messages[-1]["content"]

        relevant_chunks = get_relevant_chunks(question, k=5)

        # 🧠 Build context
        context = "\n\n".join([chunk["text"] for chunk in relevant_chunks])

        # 📄 Extract unique page numbers
        pages = sorted(set(chunk["page"] for chunk in relevant_chunks))

        if context:
            messages = [
                {
                    "role": "system",
                    "content": f"""
You are an AI tutor.

Use ONLY the context below to answer clearly.
If not found, say you don’t know.

Context:
{context}
"""
                }
            ] + messages[1:]

        answer = generate_response(messages)

        # 📌 Add citations
        if pages:
            citation_text = ", ".join([f"Page {p}" for p in pages])
            answer += f"\n\n📌 Source: {citation_text}"

        return {"response": answer}

    except Exception as e:
        return {"response": f"⚠️ Error: {str(e)}"}
