from typing import Union
from fastapi import FastAPI, Path, Body, Query, Header, HTTPException
from typing import List, Optional
from datetime import datetime
from fastapi.responses import Response

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post(
    "/v1/devices/{deviceLibraryIdentifier}/registrations/{passTypeIdentifier}/{serialNumber}"
)
def register_device(
    deviceLibraryIdentifier: str = Path(..., description="Device Library Identifier"),
    passTypeIdentifier: str = Path(..., description="Pass Type Identifier"),
    serialNumber: str = Path(..., description="Serial Number"),
    body: dict = Body(..., description="Request body"),
):
    # Mock response
    return {
        "deviceLibraryIdentifier": deviceLibraryIdentifier,
        "passTypeIdentifier": passTypeIdentifier,
        "serialNumber": serialNumber,
        "body": body,
        "status": "registered"
    }


@app.get(
    "/v1/devices/{deviceLibraryIdentifier}/registrations/{passTypeIdentifier}"
)
def check_for_updates(
    deviceLibraryIdentifier: str = Path(...),
    passTypeIdentifier: str = Path(...),
    passesUpdatedSince: Optional[str] = Query(None),
    authorization: Optional[str] = Header(None),
):
    # Mock response
    return {
        "lastUpdated": datetime.utcnow().isoformat() + "Z",
        "serialNumbers": [
         "VT434311DEC22090"
        ]
}

@app.get("/v1/passes/{passTypeIdentifier}/{serialNumber}")
async def get_pass(
    passTypeIdentifier: str = Path(...),
    serialNumber: str = Path(...),
    authorization: Optional[str] = Header(None)
):
    pkpass_path = f"./passes/{serialNumber}.pkpass"
    try:
        with open(pkpass_path, "rb") as f:
            pkpass_data = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error reading pass file")

    return Response(
        content=pkpass_data,
        media_type="application/vnd.apple.pkpass",
        headers={
            "Content-Disposition": f"attachment; filename={serialNumber}.pkpass"
        }
    )

