import sys
import time

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import logging
from typing import Union
import uvicorn

from recasepunc import CasePuncPredictor
from recasepunc import WordpieceTokenizer
from recasepunc import Config

logging.set_verbosity_error()

app = FastAPI()
predictor = CasePuncPredictor('checkpoint', lang="en")

def get_recase_punc_text(text: str, predictor: CasePuncPredictor):
    tokens = list(enumerate(predictor.tokenize(text)))
    results = ""
    for token, case_label, punc_label in predictor.predict(tokens, lambda x: x[1]):
        prediction = predictor.map_punc_label(predictor.map_case_label(token[1], case_label), punc_label)

        if token[1][0] == '\'' or (len(results) > 0 and results[-1] == '\''):
            results = results + prediction
        elif token[1][0] != '#':
            results = results + ' ' + prediction
        else:
            results = results + prediction
    return results.strip()

class Chunk(BaseModel):
    text: str

class TranscriptionChunks(BaseModel):
    data: list[Chunk]

@app.post("/vosk/transcription/recase-punc")
async def recase_punc(chunks: TranscriptionChunks):
    for chunk in chunks.data:
        chunk.text = get_recase_punc_text(chunk.text, predictor)
    return chunks

if __name__=="__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=80, log_level="info")
