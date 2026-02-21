from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import argparse
from routers import ocr

app = FastAPI(openapi_url="/api/v1/eagle-ocr/openapi.json", docs_url="/api/v1/eagle-ocr/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


app.include_router(ocr.router, prefix="/api/v1/eagle-ocr", tags=["Eagle OCR"])


@app.get("/")
async def root():
    return {"message": "Eagle OCR API"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Eagle OCR API Server")
    parser.add_argument("--port", type=int, default=8001, help="Port to run the server on (default: 8001)")
    args = parser.parse_args()

    uvicorn.run("api:app", host="0.0.0.0", port=args.port, reload=False)

# run the app with: python api.py
# go to http://127.0.0.1:8000/api/v1/eagle-ocr/docs to see the Swagger UI