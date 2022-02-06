import json
import os
from collections import defaultdict
from enum import Enum
from glob import glob
from random import randint
from typing import List, Optional

import numpy as np
from fastapi import Body, FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from model import model

mod = model.load_model()
genes = ["NRPS", "PKS"]
probably = ["This is probably a ", "It appears to be a ",
            "I'm not entirely sure, but it has the biggest chance of being a ", "Whoah, don't go too hard on me now! I think it's a "]
likely = ["It appears to have a good chance of being a ", "This is not entirely clear but I'm thinking we could have a decent chance that we're looking at a ",
          "My tinky winky sensors indicate we're looking at a ", "This would appear to have a high chance to be a "]
definitely = ["This is most definitely a ", "What is this, a copy of my training data? This is obviously a ",
              "Easy peasy lemon squeezy, this would be a ", "Do I have to fire up my CPUs for this? Ugh, okay, it's a "]
# from schemas.Course import Course

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Mode(str, Enum):
    chance = 'chance'
    specific = 'specific'
    fuzzy = 'fuzzy'


class TextIn(BaseModel):
    sequence: str = ""

    class Config:
        schema_extra = {
            "example": {
                "sequence": ">WP_003949231.1 condensation domain-containing protein, partial [Streptomyces albidoflavus]\nEALAGLVGFFVNTLALRTDTSGDPDLTTLLARVREADLAALAHQELPFEQVVSAVSPPRHPARHPLFQVM\nLALDNTPAPRATLDGLTVRRDTATGRTGAKFDLTWDLAERHTADGAPAGIGGELEYSEDLFDQATAERYA\nAQFTTLLTALLDRPDTPFTDLPFLGTRDRAAALDENGPTRPPATPDWTLTDVLATRAAADPGRTAVVDAT\nGRLTFGELQDRAERLAQRLAAAGVRPGDRVALALPRSAAALAALLGVLRAGAVHVPLDT"
            }
        }


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }


async def predict_sequence(sequence, mode):
    parsed_sequence = model.parse_input(sequence)
    # print(parsed_sequence)
    pred = mod.predict(parsed_sequence)
    match mode:
        case None:
            return str(pred)
        case "chance":
            return str(pred)
        case "specific":
            return genes[np.argmax(pred)]
        case "fuzzy":
            maxi = np.argmax(pred)
            if maxi < 0.75:
                text = probably[randint(0, 3)]
            elif maxi < 0.9:
                text = likely[randint(0, 3)]
            else:
                text = definitely[randint(0, 3)]
            return text+genes[np.argmax(pred)]
        case _:
            return mode


@app.get("/")
async def root():
    return {"message": "I am working correctly!"}


@app.put("/predict/sequences", tags=["predict"], response_model=str, summary="Predicts the genefamily of a given sequence")
async def predictSequence(sequence: TextIn, mode: Optional[Mode] = "chance"):
    """
    Provide a NRPS or PKS sequence in raw sequence format or in FASTA format.
    \n
    Note that explicit new characters are not allowed. You should convert these to new line characters (\\n)

    """
    return await predict_sequence(sequence.sequence, mode)


@ app.put("/predict/fasta_files", tags=["predict"], response_model=str, summary="Predicts the gene family of a given FASTA file")
async def predictFile(file: UploadFile, mode: Optional[Mode] = None):
    """
    Provide a NRPS or PKS sequence in a FASTA file. Just the raw sequence without FASTA header would also work
    """
    seq = await file.read()
    return await predict_sequence(seq.decode('utf-8'), mode)


@ app.put("/predict/multifasta_files", tags=["predict"], response_model=str, summary="Predicts the gene family of a given multi-FASTA file", responses={415: {"model": HTTPError, "description": "Unsupported media type. The file is probably not in FASTA format!"}})
async def predictMultiFile(file: UploadFile, mode: Optional[Mode] = None):
    """
    Provide a NRPS or PKS sequence in a multi-FASTA file. It is required that the sequences have a header line, and thus are in a legitamate format
    """
    results = defaultdict(str)
    seq = await file.read()
    seq = seq.decode('utf-8')
    if not seq.startswith(">"):
        raise HTTPException(
            415, "Unsupported media type. The file is probably not in FASTA format!")
    for sequence in seq.split(">")[1:]:
        # print(sequence)
        lines = sequence.splitlines()
        # print(lines)
        header = lines[0]
        actual_sequence = ''.join(lines[1:])
        # print(actual_sequence)
        pred = await predict_sequence(actual_sequence, mode)
        # print(pred)
        results[header.split()[0]] = str(pred)
    return JSONResponse(results)
