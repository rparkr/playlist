"""
Playlist: An app for continous text-to-speech from a provided list of URLs
(a playlist) -- helpful for long drives and learning by listening.

Created by: [Ryan Parker](https://github.com/rparkr)
"""

from fastapi import FastAPI
import httpx
import trafilatura

app = FastAPI()


@app.get(
    "/",
    summary="Load the text from a given URL",
    description=(
        "This function loads the text from a given URL and returns it for"
        " processing and chunking by later functions."
    ),
)
async def get_page_text(url: str) -> dict[str, str]:
    """
    Load the text from a given URL.

    Parameters
    ----------
    url : str
        The URL to load the text from.

    Returns
    -------
    dict[str, str]
        A dictionary containing the URL and the text loaded from the URL, in
        this format:

        ```json
        {
            "url": "https://example.com",
            "html": "<!doctype html>\n<html>\n<head>..."
        }
        ```
    """
    # Provide a default value when no URL is given
    if not url:
        return {"url": None, "text": None}
    
    # Ensure the url is properly formatted
    if not url.startswith("http"):
        url = f"https://{url}"
    
    # Make the web request
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    # Ensure the request was successful
    if not response.is_success:
        return {"url": url, "text": f"Request failed with status code: {response.status_code}"}

    # Return the text from the requested page
    return {"url": url, "html": trafilatura.extract(response.text, output_format="markdown")}


async def extract_text(raw_html: str) -> str:
    """
    Extract the text from the raw HTML.

    Parameters
    ----------
    raw_html : str
        The raw HTML to extract the text from.

    Returns
    -------
    str
        The extracted text.
    """
    return trafilatura.extract(raw_html, output_format="markdown")





# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
