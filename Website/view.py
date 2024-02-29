from flask import Blueprint, render_template,request,flash,jsonify,current_app,send_from_directory,url_for,redirect
from flask_login import login_required,current_user
from werkzeug.utils import secure_filename
import moviepy.editor as mp


import cv2
from ultralytics import YOLO
import os

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

views=Blueprint('views',__name__)



def convert_video_to_mp4(input_path, output_path):
  """Converts a video of any type to MP4 format using moviepy.

  Args:
    input_path: Path to the input video file.
    output_path: Path to the output MP4 file.

  Raises:
    IOError: If the input video file is not found or there's an issue saving the output.
  """

  try:
    clip = mp.VideoFileClip(input_path)
    clip.write_videofile(output_path)
    print("Video conversion successful using moviepy!")

  except Exception as e:
    raise IOError(f"Error converting video to MP4: {e}") from e

def delete_video_by_path(video_path):
  """
  Deletes a video file at a specified path.

  Args:
      video_path (str): The full path to the video file.

  Raises:
      OSError: If the removal operation fails.
  """

  try:
    os.remove(video_path)
    print(f"Video '{video_path}' deleted successfully.")
  except OSError as e:
    print(f"Error deleting video: {e}")




@views.route("/")
def home():
    # return "<p>test</p>"
    return render_template("home.html")


@views.route("/contact")
def contact():
    return render_template("contact.html")

@views.route("/about")
def about():
    return render_template("about.html")


# @views.route('/ahmed',methods=['GET','POST'])
# def ahmed():
#     if request.method=='POST':
#         try:
#             # Check if the request contains the file part
#             if 'videoFile' not in request.files:
#                 return jsonify({'message': 'No video file uploaded.'}), 400

#             video_file = request.files['videoFile']

#             # If user does not select file, browser also
#             # submit an empty part without filename
#             if video_file.filename == '':
#                 return jsonify({'message': 'No selected video file.'}), 400

#             # Create the upload folder if it doesn't exist
#             upload_folder = current_app.config['UPLOAD_FOLDER']
#             os.makedirs(upload_folder, exist_ok=True)

#             # Save the uploaded video file to the upload folder
#             filename = secure_filename(video_file.filename)
#             video_path = os.path.join(upload_folder, filename)
#             video_file.save(video_path)

#             os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
#             # model = YOLO('C:/Users/ahmed/PycharmProjects/Object_tracking/Single Models/YOLO_N/detect/train/weights/best.pt')
#             model = YOLO('official model/yolov8n.pt')

#             cap = cv2.VideoCapture(video_path)
#             ret=True
#         # Get the frame width and height
#             frame_width = int(cap.get(3))
#             frame_height = int(cap.get(4))
#             # fps = cap.get(cv2.CAP_PROP_FPS)

#             # aspect_ratio = frame_width / frame_height
#             # new_width = 640  # Specify your desired width
#             # new_height = int(new_width / aspect_ratio)

#             # Define output video path
#             output_video_path = os.path.join(upload_folder, 'processed_' + filename)
#             # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#             # out = cv2.VideoWriter(output_video_path, fourcc, fps, (new_width, new_height))

#             # Define the codec and create VideoWriter object
#             out = cv2.VideoWriter(output_video_path,cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width,frame_height))
            
#             while ret:
#                 ret, frame = cap.read()
#                 if ret:
#                     results = model.track(frame, persist=True)
#                     frame_ = results[0].plot()

#                     # Write the frame into the file 'output_video.avi'
#                     out.write(frame_)

#                     # Displaying frames is removed
#                     # cv2.imshow("frame", frame_)
                    
#                     if cv2.waitKey(25) & 0xFF==ord('q'):
#                         break

#             # Release everything if job is finished
#             cap.release()
#             out.release()
#             cv2.destroyAllWindows()
#             # Example usage
#             try:
#                 convert_video_to_mp4(output_video_path, "output.mp4")
#                 print("Video conversion successful!")
#             except RuntimeError as e:
#                 print(f"An error occurred: {e}")
#             # Return the URL of the processed video
#             if os.path.isfile(output_video_path):
#                 send_url=filename
#                 return render_template("New_upload.html",send_url=send_url)
#                 # processed_video_url = url_for('static', filename='uploads/processed_' + filename)
                
#             #processed_video_url = request.url_root + output_video_path
#             # return jsonify({'processed_video_url': processed_video_url}), 200

#         except Exception as e:
#             return jsonify({'message': str(e)}), 500
#     else:
#         return render_template("New_upload.html")
    

# @views.route('/serve-file/<filename>',methods=['GET'])
# def serve_file(filename):
#     return send_from_directory(current_app.config['UPLOAD_FOLDER'],filename)
    
#########################################################################
    ##################################################
    ###############


@views.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        try:
            # Check for uploaded video file
            if 'videoFile' not in request.files:
                flash('No video file uploaded.', 'Error')
                return redirect(request.url)

            video_file = request.files['videoFile']

            # Validate file selection
            if video_file.filename == '':
                flash('No selected video file.', 'Error')
                return redirect(request.url)

            # Create upload folder (if necessary)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)

            # Secure filename and generate output path
            filename = secure_filename(video_file.filename)
            video_path = os.path.normpath(os.path.join(upload_folder, filename))
            output_video_path = os.path.normpath(os.path.join(upload_folder, 'processed_' + filename))

            # Save uploaded video
            video_file.save(video_path)

            # Load YOLO model (modify path and configuration as needed)
            try:
                model = YOLO('official model/yolov8n.pt')  # Replace with correct path
            except Exception as e:
                print(f"Error loading model: {e}")
                flash('Error loading video processing model', 'Error')
                return redirect(request.url)

            # Capture video and process frames (adjust frame dimensions if needed)
            cap = cv2.VideoCapture(video_path)
            ret, frame = cap.read()

            if not ret:
                print("Error reading video frames")
                flash('Error processing video', 'Error')
                return redirect(request.url)

            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))

            # Define VideoWriter object for output video
            out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height))

            while ret:
                ret, frame = cap.read()

                if ret:
                    try:
                        # Perform object detection and tracking
                        results = model.track(frame, persist=True)
                        frame_ = results[0].plot()

                        # Write processed frame to output video
                        out.write(frame_)
                    except Exception as e:
                        print(f"Error processing frame: {e}")
                        flash('Error processing video frame', 'Error')
                        return redirect(request.url)

            # Release resources
            cap.release()
            out.release()
            cv2.destroyAllWindows()

            
            # Return response based on success/failure
            if os.path.isfile(output_video_path):
                # Attempt video conversion to MP4 (optional, handle potential errors)
                try:
                    convert_video_to_mp4(output_video_path, os.path.normpath(os.path.join(upload_folder, 'processed_Convert_' + filename)))
                    flash('Video processed successfully', 'success')
                    delete_video_by_path(output_video_path)
                    return render_template("New_upload.html", send_url=filename)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                flash('Video processing failed', 'Error')
                return redirect(request.url)
        except Exception as e:
            print(f"Unhandled error: {e}")
            flash('An internal error occurred', 'Error')
            return redirect(request.url)

    else:
        return render_template("New_upload.html")