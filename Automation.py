# Import required libraries
from AppOpener import close, open as appopen  # Import functions to open and close apps.
from webbrowser import open as webopen # Import web browser functionality.
from pywhatkit import search, playonyt  # Import functions for Google search and Youtube.
from dotenv import dotenv_values  # Import dotenv to manage environment variables.
from bs4 import BeautifulSoup  # Import beautifulSoup for parsing HTML content.
from rich import print  #Import rich for styled console output.
from groq import Groq  # Import Groq for AI chat funcionalities.
import webbrowser  # Import webbrowser for opening urls.
import subprocess # Import requests for interacting with the system.
import requests  # Import request for making HTTP requests.
import keyboard  # Import keyboard for the keyboard-related actions.
import asyncio   # Import asyncio for asynchronous programming.
import os  # Import os for operating system functionalities.

# Load environment variable from the .env file.
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")  # Retrieve the Groq API key.

# Define css classes for parsing specific elements in HTML content.
classes = ["zCubwf","hgKElc","LTKOO sY7ric", "Z0Lcw", "gsrt vk_bk FzvWsb YwPhnf", "pclqee",
           "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table", 
           "dDoNo ikb4Bb gsrt", "sxLaOe",
           "LWkfke", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Define a user-agent while making web requests.
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize the Groq client with API key.
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else i can help you with .",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
]

# List to store chatbot messages.
messages = []

# System message to provide context to the chatbot.
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. you have to write letters, codes, applications, essays, notes, songs, poems etc."}]
# Function to perform a Google search.
def GoogleSearch(topic):
    search(topic)  # Use pywhatkit's search function to perform a google search.
    return True  # Indicate success.

# Function to generate content using AI and save it to a file.
def Content(Topic): 
  
    # Nested function to open a file in Notepad.
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'  # Default text editor.
        subprocess.Popen([default_text_editor, File])  # Open the file in the default text editor.

    # Nested function to generate content using the AI chatbot.
    def ContentWriteAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})  # Add the user's prompt to messages.

        completion = client.chat.completions.create(
            model="llama3-8b-8192",  # Specify the AI model.
            messages=SystemChatBot + messages,  # Include system instructions and chat history.
            max_tokens=2048,  # Limit the maximum tokens in the response.
            temperature=0.7,  # Adjust response randomness.
            top_p=1,  # Use nucleus sampling for response diversity.
            stream=True,  # Allow the model to determine stopping conditions.
            stop=None  # Allow the model to determine stopping conditions.
        )

        Answer = ""
        for chunk in completion:
            
         if hasattr(chunk, 'choices') and chunk.choices and hasattr(chunk.choices[0], 'delta'):
            Answer += chunk.choices[0].delta.content or ""  # Safely handle None values

        Answer = Answer.replace("</s>", "")  # Remove unwanted tokens from the response.
        messages.append({"role": "assistant", "content": Answer})  # Add the AI's response to messages.
        return Answer

    Topic = Topic.replace("Content ", "")  # Remove "content" from the topic.
    ContentByAI = ContentWriteAI(Topic)  # Generate content using AI.

    # Save the generated content to a text file.
    with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)  # Write the content to the file.
        file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt")  # Open the file in Notepad.
    return True  # Indicate success.

 # Function to search for a topic on youtube.
def YoutubeSearch(Topic):
     Url4Search = f"https://www.youtube.com/results?search_query={Topic}"    # Construct the youtube search URL.
     webbrowser.open(Url4Search)  # Open the search URL in a web browser.
     return True  # Indicate success.
   
 # Function to play a video on Youtube.
def PlayYoutube(query):
     playonyt(query)  #use pywhatkit's playonyt function to play the video.
     return True   #Indicate success.

# Function to open an application or a relevant webpage.
def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)  # Attempt to open the app.
        return True  # Indicate success.
      
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML content.
            links = soup.find_all('a', {'jsname': 'UWckNb'})  # Find relevant links.
            return [link.get('href') for link in links]  # Return the extracted links.
          
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"  # Construct the Google search URL.
            headers = {"User-Agent": useragent}  # Use the predefined user-agent.
            response = sess.get(url, headers=headers)  # Perform the GET request.

            if response.status_code == 200:
                return response.text  # Return the HTML content.
            else:
                print("Failed to retrieve search results.")  # Print an error message.
            return None
          
        html = search_google(app)  # Perform the Google search.

        if html:
            links = extract_links(html)  # Extract links from the HTML.

            if links:  # Check if links exist before accessing them.
                webopen(links[0])  # Open the first available link.
                return True  # Indicate success.
            else:
                print(f"No relevant links found for {app}. Opening {app}.com")
                webopen(f"https://www.{app}.com")  # Open the official website if no search results.

        return False  # Indicate failure if no results were found.

# Function to close an application.
def CloseApp(app):
        
    if "chrome" in app:
        pass  # Skip if the app is Chrome.
    else:
      try:
          close(app, match_closest=True, output=True, throw_error=True)  # Attempt to close the app.
          return True  # Indicate success.
      except:
          return False  # Indicate Failure.
        
# Function to execute system-level commands.
def System(command):
  
    # Nested function to mute the system volume.
    def mute():
        keyboard.press_and_release("volume mute")  # Simulate the mute key press.
        
    # Nested function to unmute the system volume.
    def unmute():
        keyboard.press_and_release("volume mute")  # Simulate the unmute ey press.
        
    # Nested function to increase the system volume.
    def volume_up():
        keyboard.press_and_release("volume up")  # Simulate the volume up key press.
        
    # Nested function to decrease the system volume.
    def volume_down():
        keyboard.press_and_release("volume down")  # Simulate the volume down key press.
        
    # Execute the appropriate command.
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
        
    return True   # Indicate success.
  
# Asynchronous function to translate and execute user commands.
async def TranslateAndExecute(commands:list[str]):
  
    funcs = []  # List to store asynchronous tasks.
    
    for command in commands:
      
       if command.startswith("open "):  # Handle "open" commands.
         
           if "open it" in command:  # Ignore "open it" commands.
               pass
             
           if "open file" == command: # Ignore "open file" commands.
               pass
             
           else:
             fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))  # Schedule app opening.
             funcs.append(fun)
             
       elif command.startswith("general "):  # Placeholder for general commands.
            pass
      
       elif command.startswith("realtime "): # Placeholder for real-time commands.
            pass
          
       elif command.startswith("close "): # Handle "close" commands.
           fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))  # Schedule app closing.
           funcs.append(fun)
           
       elif command.startswith ("play "):  # Handle "play" commands.
           fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))  # Schedule Youtube playback.
           funcs.append(fun)
           
       elif command.startswith("content "):  # Handle "content" commands.
           fun = asyncio.to_thread(Content, command.removeprefix("content "))  # Schedule content creation.
           funcs.append(fun)

       elif command.startswith("google search "):  # Handle Google search commands.
           fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))  # Schedule Google search.
           funcs.append(fun)
           
       elif command.startswith("youtube search "):  # Handle Youtube search commands.
           fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search "))  # Schedule Youtube search.
           funcs.append(fun)
           
       elif command.startswith("system "): # Handle system commands.
           fun = asyncio.to_thread(System, command.removeprefix("system "))  # Schedule system command.
           funcs.append(fun)
           
       else:
           print(f"No Function Found. For {command}")  # Print an error for unrecognized commands.
           
    results = await asyncio.gather(*funcs)  # Execute all tasks concurrently.
  
    for result in results:  # Process the results.
      if isinstance(result, str):
         yield result
      else:
         yield result
         
# Asynchronous function to automate command execution.
async def Automation(commands: list[str]):
  
    async for results in TranslateAndExecute(commands):

        pass
      
    return True  # Indicate success.

if __name__ == "__main__":
    asyncio.run(Automation(["content for me"]))