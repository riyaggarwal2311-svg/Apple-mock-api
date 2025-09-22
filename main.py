from typing import Union

from fastapi import FastAPI, Path, Body

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
