import logging

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.application.settings import settings
from backend.application.views import (
    dependencies, auth, ad, complaint, comment, user
)

app = FastAPI(title="Ad Service", description="Test",
              debug=settings.DEBUG)

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(auth.web_router)
app.include_router(user.web_router)
app.include_router(ad.web_router)
app.include_router(comment.web_router)
app.include_router(complaint.web_router)

app.add_event_handler('startup', dependencies.start)
app.add_event_handler('shutdown', dependencies.stop)

if __name__ == "__main__":
    uvicorn.run(
        "app:app", host="localhost", port=5000, reload=True,
        log_level=logging.INFO
    )
