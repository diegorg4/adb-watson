import os
from common.log_event import log_event

from fastapi.responses import FileResponse
from fastapi import HTTPException

def fetch_tickets(file_uuid: str):

    file_path = os.path.join( os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              "files", 
                              f"{file_uuid}.pdf" )

    log_event(F"UUID: {file_uuid} \n Trying to fetch {file_path}",log_internal=True)

    if(os.path.exists(file_path)):

        return  FileResponse(file_path, filename="downloaded_file.pdf", 
                             media_type="application/pdf", 
                             headers={"Content-Type":"application/pdf"}
                             )
    
    else:

        raise HTTPException(status_code=400, detail="File does not exists", headers={"Content-Type":"application/pdf"})
