import streamlit as st
import asyncio
from typing import Optional, List
from graphlit_api import *
import requests
import jwt
import datetime

def run_async_task(async_func, *args):
    """
    Run an asynchronous function in a new event loop.

    Args:
    async_func (coroutine): The asynchronous function to execute.
    *args: Arguments to pass to the asynchronous function.

    Returns:
    None
    """
    
    loop = None

    try:
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(async_func(*args))
    except:
        # Close the existing loop if open
        if loop is not None:
            loop.close()

        # Create a new loop for retry
        loop = asyncio.new_event_loop()

        return loop.run_until_complete(async_func(*args))
    finally:
        if loop is not None:
            loop.close()

def render_citations(citations: Optional[List[Optional[PromptConversationPromptConversationMessageCitations]]]):
    for citation in citations:
        emoji = select_emoji(citation.content.type, citation.content.file_type)
        index_emoji = index_to_emoji(citation.index)

        if citation.page_number is not None:
            expander_label = f"{index_emoji} {emoji} {citation.content.file_name}: Page {citation.page_number}"
        else:
            expander_label = f"{index_emoji} {emoji} {citation.content.file_name}"
        
        with st.expander(expander_label):            
            st.markdown(citation.text)

def select_emoji(content_type, file_type):
    # Emoji mappings for content types
    content_emoji_map = {
        "FILE": "📄",  # Default for files, overridden by specific file types below
        "PAGE": "🌐",
        "MESSAGE": "💬",
        "TEXT": "📝",
        "POST": "📰",
        "EMAIL": "📧",
        "EVENT": "📅",
        "ISSUE": "🐛",
    }

    # Emoji mappings for file types (used only if content_type is "FILE")
    file_emoji_map = {
        "VIDEO": "🎥",
        "AUDIO": "🎵",
        "IMAGE": "🖼️",
        "DOCUMENT": "📃",
        "EMAIL": "📧",
        "CODE": "💻",
        "DATA": "📊",
    }

    # Select the appropriate emoji
    if content_type == "FILE" and file_type is not None:
        # Return the emoji corresponding to the specific file type
        return file_emoji_map.get(file_type, "📄")
    else:
        # Return the emoji corresponding to the content type
        return content_emoji_map.get(content_type, "📄")

def index_to_emoji(index):
    # Mapping of index to emoji numbers
    emoji_map = {
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
        10: "🔟",
    }
    # Return the emoji, or the index itself if no emoji available
    return emoji_map.get(index, index)

def get_file_types_documents():
    """
    Show the supported file types for documents.
    """
    
    markdown_text = """
| File Type               | File Extension       |
|-------------------------|----------------------|
| PDF                     | .pdf                 |
| HTML                    | .htm .html           |
| MIME Archive            | .mhtml               |
| Word Document           | .docx                |
| Excel Spreadsheet       | .xlsx                |
| PowerPoint Presentation | .pptx                |
| Rich Text Format        | .rtf                 |
| Markdown                | .md                  |
| Text                    | .txt .text           |
| Comma-Separated Values  | .csv                 |
| Tab-Separated Values    | .tsv                 |
| Log File                | .log                 |
"""
    return markdown_text, "PDF files will automatically extract and ingest any embedded images, upon file preparation."
       
def get_file_types_audio():
    """
    Show the supported file types for audio.
    """
    
    markdown_text = """
| File Type             | File Extension        |
|-----------------------|-----------------------|
| WAV                   | .wav                  |
| MPEG-4 Audio          | .m4a .aac .mp4        |
| MPEG Audio            | .mpa .m2a             |
| MP3                   | .mp3                  |
| FLAC                  | .flac                 |
| OGG                   | .ogg .opus            |
| AIFF                  | .aiff .aifc .aif      |
| AC-3                  | .ac3                  |
| Windows Media Audio   | .wma                  |
"""
    return markdown_text, None
    
def get_file_types_video():
    """
    Show the supported file types for video.
    """
    
    markdown_text = """
| File Type        | File Extension   |
|------------------|------------------|
| MPEG-4           | .mp4             |
| QuickTime Video  | .mov .moov .qt   |
"""
    return markdown_text, None        

def get_file_types_images():
    """
    Show the supported file types for images.
    """
    
    markdown_text = """
| File Type        | File Extension      |
|------------------|---------------------|
| JPEG             | .jpg .jpeg .jpe     |
| PNG              | .png                |
| HEIC             | .heif .heic         |
| WebP             | .webp               |
| Windows Bitmap   | .bmp                |
| TIFF             | .tif .tiff          |
"""
    return markdown_text, None
   
def get_file_types_animations():
    """
    Show the supported file types for animations.
    """
    
    markdown_text = """
| File Type     | File Extension |
|---------------|----------------|
| GIF           | .gif           |
| Animated PNG  | .apng          |
""" 
    return markdown_text, None
    
def get_file_types_data():
    """
    Show the supported file types for data.
    """
    
    markdown_text = """
| File Type | File Extension |
|-----------|----------------|
| JSON      | .json          |
| XML       | .xml           |
"""
    return markdown_text, None
     
def get_file_types_emails():
    """
    Show the supported file types for emails.
    """
    
    markdown_text = """
| File Type | File Extension |
|-----------|----------------|
| EML       | .eml           |
| MSG       | .msg           |
"""
    return markdown_text, "Emails will automatically extract and ingest any attached files, upon file preparation."  
    
def get_file_types_code():
    """
    Show the supported file types for code.
    """
    
    markdown_text = """
| File Type   | File Extension |
|-------------|----------------|
| Python      | .py            |
| JavaScript  | .js            |
| TypeScript  | .ts            |
| Go          | .go            |
| C#          | .cs            |
| C           | .c             |
| C++         | .cpp           |
| Java        | .java          |
| PHP         | .php           |
| Ruby        | .rb            |
| Swift       | .swift         |
| Rust        | .rs            |
"""
    return markdown_text, "Graphlit recognized 50+ code file extensions.  If you find a code file extension we don't support, please reach out to us and we will add it."
    
def get_file_types_packages():
    """
    Show the supported file types for packages.
    """
    
    markdown_text = """
| File Type | File Extension |
|-----------|----------------|
| ZIP       | .zip           |
"""
    return markdown_text,"Packages will automatically extract and ingest any packaged files, upon file preparation."
    
def get_file_types_other():
    """
    Show the supported file types for other files.
    """
    
    markdown_text = """
| File Type                   | File Extension        |
|-----------------------------|-----------------------|
| Design Web Format           | .dwf .dwfx            |
| AutoCAD DXF                 | .dxf                  |
| Autodesk Drawing            | .dwg                  |
| SVG                         | .svg                  |
| GeoJSON                     | .geojson              |
| ESRI Shapefile              | .shp                  |
| Autodesk FBX                | .fbx                  |
| 3D Studio                   | .3ds                  |
| Collada                     | .dae                  |
| GL Transmission Format      | .gltf .glb            |
| Google Draco                | .drc                  |
| Wavefront                   | .obj                  |
| 3D Systems CAD              | .stl                  |
| Universal Scene Description | .usdz                 |
| LAS                         | .las .laz             |
| E57                         | .e57                  |
| PTS                         | .ptx .pts             |
| PLY                         | .ply                  |
"""
    return markdown_text, None

def select_file_types(table_to_show):
    # Display the supported file types based on the selected table
    if table_to_show == "Documents":
        file_types_table, extra_info = get_file_types_documents()
        file_types = ["pdf","htm","html","mhtml","docx","xlsx","pptx","rtf","md","txt","text","csv","tsv","log"]
    elif table_to_show == "Audio":
        file_types_table, extra_info  = get_file_types_audio()
        file_types = ["wav","m4a","aac","mp4","mpa","m2a","mp3","flac","ogg","opus","aiff","aifc","aif","ac3","wma"]
    elif table_to_show == "Video":
        file_types_table, extra_info  = get_file_types_video()
        file_types = ["mp4","mov","moov","qt"]            
    elif table_to_show == "Images":
        file_types_table, extra_info  = get_file_types_images()
        file_types = ["jpg","jpeg","jpe","png","heif","heic","webp","bmp","tif","tiff"]
    elif table_to_show == "Animations":
        file_types_table, extra_info  = get_file_types_animations()      
        file_types = ["gif","apng"]      
    elif table_to_show == "Data":
        file_types_table, extra_info  = get_file_types_data()
        file_types = ["json","xml"]
    elif table_to_show == "Emails":
        file_types_table, extra_info  = get_file_types_emails()
        file_types = ["eml","msg"]
    elif table_to_show == "Code":
        file_types_table, extra_info  = get_file_types_code()
        file_types = ["py","js","ts","go","cs","c","cpp","java","php","rb","swift","rs"]
    elif table_to_show == "Packages":
        file_types_table, extra_info  = get_file_types_packages()
        file_types = ["zip"]
    elif table_to_show == "Other":
        file_types_table, extra_info  = get_file_types_other()
        file_types = ["dwf","dwfx","dxf","dwg","svg","geojson","shp","fbx","3ds","dae","gltf","glb","drc","obj","stl","usdz","las","laz","e57","ptx","pts","ply"]

    return file_types, file_types_table, extra_info

def show_file_type_table(markdown_table):
    """ 
    Display the markdown table full width.
    """
    
    st.markdown("""
<style>
/* Target all tables within the Streamlit app and set them to full width */
table {
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)
    
    # Display the table in Streamlit using Markdown
    st.markdown(markdown_table, unsafe_allow_html=True)


def query_contents(filter):
    """
    Perform a GraphQL query to get contents.

    Args:
    filter (dict): The filter to apply to the query.

    Returns:
    list: A list of content results.
    """
    query = """
    query QueryContents($filter: ContentFilter!) {
      contents(filter: $filter) {
        results {
          id
          name
          format # eg PDF
          formatName # eg Portable Document Format
          fileExtension # eg .pdf
        }
      }
    }
    """

    url = "https://data-scus.graphlit.io/api/v1/graphql"

    # Define the issuer and audience
    issuer = "graphlit"
    audience = "https://portal.graphlit.io"

    # Specify the role (Owner, Contributor, Reader)
    role = "Owner"

    # Specify the expiration (one hour from now)
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    # Define the payload
    payload = {
        "https://graphlit.io/jwt/claims": {
            "x-graphlit-environment-id": st.secrets["environment_id"],
            "x-graphlit-organization-id": st.secrets["organization_id"],
            "x-graphlit-role": role,
        },
        "exp": expiration,
        "iss": issuer,
        "aud": audience,
    }

    # Sign the JWT
    token = jwt.encode(payload, st.secrets["jwt_secret"], algorithm="HS256")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    graphql_payload = {
        'query': query,
        'variables': {'filter': filter}
    }

    try:
        response = requests.post(url, json=graphql_payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None

    # Example usage
    filter = {
        # Your filter here
    }
    results = query_contents(filter)
    if results:
        st.write("Query succeeded:", results)
    else:
        st.write("Query failed.")

def query_contents_count(filter):
    """
    Perform a GraphQL query to get the count of contents.

    Args:
    filter (dict): The filter to apply to the query.

    Returns:
    int: The count of contents.
    """
    query = """
    query QueryContents($filter: ContentFilter!) {
      countContents {
        count
      }
    }
    """

    url = "https://data-scus.graphlit.io/api/v1/graphql"

    # Define the issuer and audience
    issuer = "graphlit"
    audience = "https://portal.graphlit.io"

    # Specify the role (Owner, Contributor, Reader)
    role = "Owner"

    # Specify the expiration (one hour from now)
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    # Define the payload
    payload = {
        "https://graphlit.io/jwt/claims": {
            "x-graphlit-environment-id": st.secrets["environment_id"],
            "x-graphlit-organization-id": st.secrets["organization_id"],
            "x-graphlit-role": role,
        },
        "exp": expiration,
        "iss": issuer,
        "aud": audience,
    }

    # Sign the JWT
    token = jwt.encode(payload, st.secrets["jwt_secret"], algorithm="HS256")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    graphql_payload = {
        'query': query,
        'variables': {'filter': filter}
    }

    try:
        response = requests.post(url, json=graphql_payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data['data']['countContents']['count'] if 'data' in data and 'countContents' in data['data'] else None
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None


