"""
Application Main file.

In the challenge/main.py file, define an entry point \
    for running the application.
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="127.0.0.1", port=8000, reload=True)
