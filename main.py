from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from resume_parser import extract_resume_info, extract_text_from_pdf
from database import  Session as SessionLocal, base, new_person

app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/parse_resume/")
async def parse_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    print(" /parse_resume/ endpoint was hit!")

    try:
        file_bytes = await file.read()

        if file.filename.endswith(".pdf"):
            print(" PDF detected, extracting text...")
            resume_text = extract_text_from_pdf(file_bytes)
        else:
            print("📄 Treating file as plain text...")
            resume_text = file_bytes.decode("utf-8")

        print(" Extracted text:\n", resume_text[:500])

        print(" Sending to LLM agent...")
        parsed_result = extract_resume_info(resume_text)

        print(" Parsed result:\n", parsed_result)

        person = new_person(
            name=parsed_result.get("name", ""),
            Email=parsed_result.get("Email", ""),
            Phone_number=parsed_result.get("Phone_number", None),
            Skills=parsed_result.get("Skills", ""),
            Education=parsed_result.get("Education", ""),
            Work_experience=parsed_result.get("Work_experience", 0),
            achievements=parsed_result.get("achievements", "N/A"),
            job_position=parsed_result.get("job_position", "")
        )

        db.add(person)
        db.commit()
        db.refresh(person)

        return {"parsed_resume": parsed_result, "message": " Stored in database"}

    except Exception as e:
        print(" Exception occurred in /parse_resume/:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
