import os
import tkinter
import customtkinter
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip

def merge_files_moviepy(video_path, audio_path, output_path):
    try:
        # Load the video and audio files
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        
        # Set the audio of the video clip to the audio clip
        video_clip = video_clip.set_audio(audio_clip)
    

        # Write the merged video and audio to the output path
        video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        
        # Close the clips
        video_clip.close()
        audio_clip.close()
        
        print(f"Video and audio merged successfully: {output_path}")
    
    except Exception as e:
        print(f"Failed to merge video and audio: {e}")
        finishLabel.configure(text=f"Erreur de fusion: {e}", text_color="red")

# Function for download
def startDownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        
        # Determine the selected type and quality
        selected_type = stream_type.get()
        selected_quality = quality.get()
        
        # Initialize variables for paths
        video_path = None
        audio_path = None
        
        # Download streams based on selected options
        if selected_type == "Audio":
            audio_stream = ytObject.streams.filter(only_audio=True).first()
            if audio_stream:
                audio_path = audio_stream.download("YoutubeDownload")
                print(f"Downloaded audio file: {audio_path}")
            else:
                print(f"No audio stream found at selected quality: {selected_quality}")
        elif selected_type == "Video":
            video_stream = ytObject.streams.filter(file_extension='mp4', res=selected_quality).first()
            if video_stream:
                video_path = video_stream.download("YoutubeDownload/Video")
                print(f"Downloaded video file: {video_path}")

                audio_stream = ytObject.streams.filter(only_audio=True).order_by('abr').desc().first()
                if audio_stream:
                    audio_path = audio_stream.download("YoutubeDownload/Audio")
                    print(f"Downloaded audio file: {audio_path}")
            else:
                print(f"No video stream found at selected quality: {selected_quality}")
        
        # Debugging file paths and check if files exist
        if video_path:
            print(f"Video path: {video_path}")
        if audio_path:
            print(f"Audio path: {audio_path}")
            
        if not video_path or not audio_path:
            print("Error: Could not download video or audio streams.")
            finishLabel.configure(text="Le lien est invalide !", text_color="red")
            return
        
        # Sanitize video title for file paths
        title_sanitized = ytObject.title.replace('/', '_').replace('\\', '_')
        output_path = f"YoutubeDownload/{title_sanitized}.mp4"
        
        # Merge video and audio
        merge_files_moviepy(video_path, audio_path, output_path)
        finishLabel.configure(text="Téléchargement Réussie !", text_color="green")
        
        # Remove audio and video files when merging files
        os.remove(audio_path)
        os.remove(video_path)
        print(f"Deleted files: {audio_path} and {video_path}")

    except Exception as e:
        finishLabel.configure(text=f"Le lien est invalide !: {str(e)}", text_color="red")
        print(f"Exception occurred: {e}")


# Function for the progress bar
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    pPercentage.configure(text=per + '%')
    pPercentage.update()
    
    # Update progress bar
    progressBar.set(percentage_of_completion / 100)

# Initialize the tkinter application
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("720x240")
app.title("YouTube Downloader")

# Add UI elements
title = customtkinter.CTkLabel(app, text="Insérer un lien YouTube")
title.pack(padx=10, pady=10)

# Input for the link
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# Label for the end of the download
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# Progress bar
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack()

# Create select options for stream type and quality
stream_type = tkinter.StringVar(value="Audio")  # Default to "Video"
quality = tkinter.StringVar(value="720p")  # Default to "720p"

# Frame to hold the select options
select_frame = customtkinter.CTkFrame(app)
select_frame.pack(padx=10, pady=10)

# Stream type select (Audio/Video)
stream_type_select = customtkinter.CTkOptionMenu(select_frame, variable=stream_type, values=["Audio", "Video"])
stream_type_select.pack(side=tkinter.LEFT, padx=10)

# Quality select (720p/1080p)
quality_select = customtkinter.CTkOptionMenu(select_frame, variable=quality, values=["720p", "1080p"])
quality_select.pack(side=tkinter.LEFT, padx=10)

# Download button
download = customtkinter.CTkButton(app, text="Télécharger", command=startDownload)
download.pack(padx=10, pady=10)

# Mainloop of the application
app.mainloop()